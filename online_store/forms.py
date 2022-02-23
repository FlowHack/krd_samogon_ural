from django import forms
from online_store.models import Product


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['pub_date']

    #def clean_characteristics(self):
     #   super(ProductAdminForm, self).clean()
#
 #       characteristics = self.cleaned_data.get('characteristics')
  #      subcategory = self.cleaned_data.get('subcategory')
   #     need_characteristics = subcategory.characteristics.all()
    #    name_need = ', '.join([str(item) for item in need_characteristics])
#
 #       length_characteristics = len(characteristics)
  #      length_need = len(need_characteristics)
#
 #       if length_characteristics != length_need:
  #          raise forms.ValidationError(
   #             'Указаны неверные характеристики продукта. Должны быть '
    #            f'указаны те же, что и у подкатегории: {name_need}'
     #       )
#
 #       return self.cleaned_data
