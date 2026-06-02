import csv, io, os, json
from .utils import get_coverage

from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from dotenv import load_dotenv
load_dotenv()

from .models import Course, Problem, Module

from groq import Groq
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
#from openai import OpenAI
#client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


REQUIRED_COLUMNS = {'input', 'expected_output', 'marks', 'type'}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TESTCASE_PROMPT = open(os.path.join(BASE_DIR, 'prompts', 'testcase_prompt.txt')).read()
EDGECASE_PROMPT = open(os.path.join(BASE_DIR, 'prompts', 'edgecase_prompt.txt')).read()
SYLLABUS_PROMPT = open(os.path.join(BASE_DIR, 'prompts', 'syllabus_prompt.txt')).read()



# .csv part
@api_view(['POST'])
def upload_csv(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'error': 'No file uploaded'}, status=400)
    if not file.name.endswith('.csv'):
        return Response({'error': 'Invalid file format. Please upload a CSV file.'}, status=400)
    
    dataFile = file.read().decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(dataFile))
    

    if csv_reader.fieldnames is None:
        return Response({'error': 'CSV file has no header'}, status=400)
    
    cleaned_fields = {f.strip().lower() for f in csv_reader.fieldnames}

    if not REQUIRED_COLUMNS.issubset(cleaned_fields):
        return Response({'error': f'Missing required columns. Required columns are: {REQUIRED_COLUMNS}'}, status=400)


    success_rows = []
    error_rows = []

    for row_num, row in enumerate(csv_reader, start=2):
        input_value = row.get('input', '').strip()
        expected_output = row.get('expected_output', '').strip()
        marks = row.get('marks', '').strip()
        type_value = row.get('type', '').strip()

        if not input_value or not expected_output or not marks or not type_value:
            error_rows.append({'row': row_num, 'error': 'Missing required fields'})
            continue

        try:
            marks = int(marks)
        except ValueError:
            error_rows.append({'row': row_num, 'error': 'Marks must be an integer'})
            continue
        
        type_value = type_value.lower()
        if type_value not in ['normal', 'edge', 'corner']:
            error_rows.append({'row': row_num, 'error': f'Invalid type: {type_value}. Must be normal, edge or corner'})
            continue

        success_rows.append({
            'input': input_value,
            'expected_output': expected_output,
            'marks': marks,
            'type': type_value
        })

    return Response({
    'success_count': len(success_rows),
    'success_rows': success_rows,
    'error_count': len(error_rows),
    'errors': error_rows
})





# Arranging syllabus in a hierarchical manner using AI
@api_view(['POST'])
def upload_syllabus(request):
    course_name = request.data.get('course_name')
    course_level = request.data.get('course_level')
    raw_syllabus = request.data.get('syllabus')

    if not course_name:
        return Response({'error': 'Course name is required'}, status=400)
    if not course_level:
        return Response({'error': 'Course level is required'}, status=400)
    if not raw_syllabus:
        return Response({'error': 'Syllabus is required'}, status=400)
    
    syllabus_message = SYLLABUS_PROMPT.replace("{{SYLLABUS_TEXT}}", raw_syllabus)
    
    syllabus_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        #model="meta-llama/Llama-2-7b-hf",
        messages=[{"role": "user", "content": syllabus_message}],
        temperature=0.4,
    )

    structured_syllabus = syllabus_response.choices[0].message.content

    try:
        cleaned = structured_syllabus.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        structured_syllabus = json.loads(cleaned.strip())
    except json.JSONDecodeError:
        return Response({'error': 'Failed to parse response from AI', 'raw': structured_syllabus}, status=500)

    try:
        course = Course.objects.create(
            course_name=course_name,
            course_level=course_level,
            syllabus=structured_syllabus
        )
    except Exception as e:
        return Response({'error': f'Failed to save course: {str(e)}'}, status=500)

    return Response({
        'message': 'Syllabus uploaded successfully',
        'course_id': course.id,
        'course_name': course.course_name,
        'syllabus': structured_syllabus
    })




# Generating test cases using AI
@api_view(['POST'])
def generate_testcases(request):

    problem_statement = request.data.get('problem_statement')
    input_format = request.data.get('input_format')
    output_format = request.data.get('output_format')
    constraints = request.data.get('constraints')

    if not problem_statement:
        return Response({'error': 'Problem statement is required'}, status=400)
    if not input_format:
        return Response({'error': 'Please provide input format'}, status=400)
    if not output_format:
        return Response({'error': 'Please provide output format'}, status=400)
    if not constraints:
        return Response({'error': 'Constraints are required'}, status=400)
    
    course_id = request.data.get('course_id')
    module_tags = request.data.get('module_tags')

    coverage = None
    if course_id and module_tags:
        coverage = get_coverage(course_id, module_tags)

    testcase_message = TESTCASE_PROMPT + f"""
            Problem Statement: {problem_statement}
            Input Format: {input_format}
            Output Format: {output_format}
            Constraints: {constraints}
            """
    testcase_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        #model="meta-llama/Llama-2-7b-hf",
        messages=[{"role": "user", "content": testcase_message}],
        temperature=0.3,
    )

    test_cases = testcase_response.choices[0].message.content

    try:
            cleaned = test_cases.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            data = json.loads(cleaned.strip())
            return Response(data)
    except json.JSONDecodeError:
            return Response({'error': 'Failed to parse response from AI', 'raw': test_cases}, status=500)







# Generating edge cases using AI
@api_view(['POST'])
def generate_edgecases(request):
    problem_statement = request.data.get('problem_statement')
    input_format = request.data.get('input_format')
    output_format = request.data.get('output_format')
    constraints = request.data.get('constraints')

    if not problem_statement:
        return Response({'error': 'Problem statement is required'}, status=400)
    if not input_format:
        return Response({'error': 'Please provide input format'}, status=400)
    if not output_format:
        return Response({'error': 'Please provide output format'}, status=400)
    if not constraints:
        return Response({'error': 'Constraints are required'}, status=400)
    
    edgecase_message = EDGECASE_PROMPT + f"""
            Problem Statement: {problem_statement}
            Input Format: {input_format}
            Output Format: {output_format}
            Constraints: {constraints}
            """
    edgecase_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        #model="meta-llama/Llama-2-7b-hf",
        messages=[{"role": "user", "content": edgecase_message}],
        temperature=0.3,
    )
    edge_cases = edgecase_response.choices[0].message.content
    try:
            cleaned = edge_cases.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            data = json.loads(cleaned.strip())
            return Response(data)
    except json.JSONDecodeError:
            return Response({'error': 'Failed to parse response from AI', 'raw': edge_cases}, status=500)
    
