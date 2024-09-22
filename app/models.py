from django.db import models

class Analysis(models.Model):
    name = models.CharField(max_length=255, help_text="Name of analysis")

class File(models.Model):
    # Fields
    path = models.CharField(max_length=255, help_text="File path on the server or storage")
    uri = models.CharField(max_length=255, help_text="File URI (uniform resource identifier)")
    url = models.URLField(max_length=500, help_text="Publicly accessible URL to the file")
    tags = models.JSONField(null=True, blank=True, help_text="Tags as a JSON array")
    size = models.BigIntegerField(help_text="File size in bytes")
    analysis = models.ForeignKey(Analysis, null=True, on_delete=models.CASCADE, related_name='files')

    # Metadata
    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"

    # String representation
    def __str__(self):
        return f"File: {self.path} (Size: {self.size} bytes)"
    
