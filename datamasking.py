from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Masting data for security
class DataMasking:
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    # Masking data
    @classmethod
    def masking(cls, str):
        #Keep DATE and TIME data
        configs={"DATE_TIME": OperatorConfig("keep"),"IN_PAN": OperatorConfig("keep")}
        result_analyzer = cls.analyzer.analyze(text=str, entities=None, language="en")
        result_anonymizer = cls.anonymizer.anonymize(text=str, analyzer_results=result_analyzer,operators=configs)
        return result_anonymizer.text

