from . models import AdminDocumentData
from . serializers import AdminDocumentDataSerializer
def findAdminDocument(id):
    try:
        document = AdminDocumentData.objects.get(admin_id = id)
        documentSerializer = AdminDocumentDataSerializer(document)
        return documentSerializer.data, True

    except AdminDocumentData.DoesNotExist:
        return {"error": "admin document not found"}, False
    