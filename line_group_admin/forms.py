from django import forms

from .models import LineGroup


class LineGroupForm(forms.ModelForm):
    class Meta:
        model = LineGroup
        fields = ('line_group_name', 'emba_group_name')

    def __init__(self, *args, **kwargs):
        # django widget 的 Customizing widget instances
        # 自己增加需要的欄位ex: class, id
        super().__init__(*args, **kwargs)
        self.fields['line_group_name'].widget.attrs.update(
            {'class': 'form-control mr-sm-2', 'id': 'InputLineGroup'}
        )
        self.fields['emba_group_name'].widget.attrs.update(
            {'class': 'form-control mr-sm-2', 'id': 'InputEmbaGroup'}
        )
