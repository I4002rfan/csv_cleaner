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