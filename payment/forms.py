from django import forms

from payment.models import Fee, Payment


class DateInput(forms.DateInput):
    input_type = 'date'

class SetFeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = '__all__'
        labels = {
            'fee': 'Такса',
            'deadline': 'Срок на плащане'
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("card_number", "card_cvv", "card_expiry_date")
        labels = {
            'card_expiry_date': 'Срок на валидност (YYYY-mm-dd)',
        }
        # card_expiry_date = forms.DateField(
        #
        #         label='Card Expiry Date (YYYY-mm-dd)',
        #
        # )
        # card_expiry_date = forms.DateInput(
        #     format=('%Y-%m-%d'),
        #     attrs={
        #            'type': 'date'
        #            },
        # )
