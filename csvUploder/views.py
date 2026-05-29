from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

import csv, io

REQUIRED_COLUMNS = {'input', 'expected_output', 'marks', 'type'}


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
    
    #Integrate bodhibot....

    return Response({"test_cases": [
        {
            'id': 1,
            'input': '1 2\n3 4',
            'expected_output': '10',
            'constraints': '1 <= a, b, c, d <= 1000',
            'marks': 10,
            'type': 'normal',
            'notes': 'This is a sample test case generated based on the provided problem statement and constraints.',
        },
        {
            'id': 2,
            'input': '5 6\n7 8',
            'expected_output': '26',
            'constraints': '1 <= a, b, c, d <= 1000',
            'marks': 10,
            'type': 'normal',
            'notes': 'This is another sample test case generated based on the provided problem statement and constraints.',
        },
        {
            'id': 3,
            'input': '100 200\n300 400',
            'expected_output': '1000',
            'constraints': '1 <= a, b, c, d <= 1000',
            'marks': 10,
            'type': 'normal',
            'notes': 'This is a third sample test case generated based on the provided problem statement and constraints.',
        }
    ]})


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
    
    #Integrate bodhibot....

    return Response({"edge_cases": [
        {
            'id': 1,
            'input': '0 0\n0 0',
            'expected_output': '0',
            'constraints': '1 <= a, b, c, d <= 1000',
            'edge_type': 'max',
            'notes': 'This test case checks the behavior of the solution when all inputs are at their minimum values.'
        },
        {
            'id': 2,
            'input': '1000 1000\n1000 1000',
            'expected_output': '4000000000',
            'constraints': '1 <= a, b, c, d <= 1000',
            'edge_type': 'min',
            'notes': 'This test case checks the behavior of the solution when all inputs are at their maximum values.'
        },
        {
            'id': 3,
            'input': '-1 -1\n-1 -1',
            'expected_output': '-4',
            'constraints': '-1000 <= a, b, c, d <= -1',
            'edge_type': 'negative',
            'notes': 'This test case checks the behavior of the solution when all inputs are negative values.'
        }
    ]})  