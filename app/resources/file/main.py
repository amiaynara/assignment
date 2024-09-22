"""DRF File viewset"""

# Lib imports
import json
import os
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from sqlite_s3_query import sqlite_s3_query

# App imports
from app.models import File
from app.resources.file.serializer import FileSerializer

class FileViewSet(viewsets.ModelViewSet):
    """File viewset"""

    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_object(self):
        """Override to get the file object"""
        # Need to check if this extra condition of tags__icontains can be replaced by FilterSet
        queryset = self.filter_queryset(self.get_queryset())
        # Perform the lookup filtering.
        obj = get_object_or_404(queryset, analysis=self.kwargs.get("analysis_id"), tags__icontains=self.request.query_params.get("tags"))
        self.check_object_permissions(self.request, obj)
        return obj
    
    @action(detail=False, methods=["get"], url_path="initial-data")
    def initial_data(self, request, **kwargs):
        """Get initial data from the sqlite file"""
        sort_dict = {"VARIANT_ID": "asc"}
        query_dict = {"variants": {}}
        offset = 0
        file_obj = self.get_object()
        # conf = self.get_config(config_file)
        queries = self.get_query()
        result = self.execute_query(file_obj.uri, queries)
        response_data = {"initial_data": result, "analysis": file_obj.analysis.name}
        return Response(response_data)
    
    def get_query(self):
        '''Retuns the query to be executed on the file'''
        query = '''
            SELECT ALT.ALT_AF, ALT.alt_gene, ALT.ALT_TYPE, variants.INFO_DP, variants.CHROM, variants.POS, variants.ID, variants.REF, variants.QUAL, variants.VARIANT_ID, annotations.Annotation, annotations.Annotation_Impact, annotations.Gene_Name, annotations.Feature_Type, annotations.Feature_ID, annotations.Transcript_BioType, annotations."HGVS.p"
                        FROM variants
                        JOIN ALT ON variants.VARIANT_ID = ALT.VARIANT_ID JOIN annotations ON variants.VARIANT_ID = annotations.VARIANT_ID JOIN sample ON variants.VARIANT_ID = sample.VARIANT_ID
                        WHERE variants.VARIANT_ID IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100)
            '''
        return query
    
    def execute_query(self, file_uri, queries):
        '''Method to executet the sql raw query'''

        file_uri = 'https://variant-testing-1.s3.amazonaws.com/analyses/461/40418/parser/Control1_fastq.GRCh38.variants.w_AF.annotated.db'
        config_file_uri = 'https://variant-testing-1.s3.amazonaws.com/analyses/461/40418/parser/Control1_fastq.GRCh38.variants.w_AF.annotated.config.json'
        # query_string = "SELECT name FROM sqlite_master WHERE type='table';"
        result = None
        if not isinstance(queries, list):
            queries = [queries]
        print('the queries are: ', queries)
        results = []
        with sqlite_s3_query(file_uri) as query:
            for query_string in queries:
                with query(query_string) as (columns, rows):
                    result = [row for row in rows]
                    results.append(result)
        return results

    def get_conf(self):
        '''An implementation to read the config file from the local'''
        config_file = File.objects.get(analysis='', tags__icontains='')
        config_file_name = 'Control1_fastq.GRCh38.variants.w_AF.annotated.config.json'
        folder = '/Users/amiaynarayan/work/webapp/www/variant'
        config_path = os.path.join(folder, config_file_name)
        f = open(config_path)
        config = json.loads(f.read())
        display_col_config = config["COLUMN_CONFIG"]
        return display_col_config
    