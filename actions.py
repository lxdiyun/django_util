from django.http import HttpResponse
from admin_actions import prep_field
from utils import UnicodeWriter


def export_as_csv(filename, field_names, queryset, header=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
            unicode(filename).replace('.', '_')
        )

        writer = UnicodeWriter(response)

        if header:
            writer.writerow(header)

        for obj in queryset:
            writer.writerow([prep_field(obj, field) for field in field_names])

        return response
