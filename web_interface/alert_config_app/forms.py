"""forms.py defines the input fields for data entry pages generated by Django.

The classes contained here describe sets of data entry fields that django uses
to construct form pages and validate the incoming information.

Note
____
    Fields referencing databse entries (e.g. new_pv's use of PV.objects.all())
    MUST be placed inside the init funciton. Failure to do
    so will break djang's ability to migrate and has the potential to interfere
    with other features. 

"""

from django import forms
from .models import Alert, Pv, Trigger#, PVname
from account_mgr_app.models import Profile
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .widgets import HorizontalCheckbox


class configTrigger(forms.Form):
    """Define the fields for an individual trigger

    Attributes
    __________
        new_pv : forms.ChoiceField
            Provides dropdown selection of PV's to link to this trigger. This 
            attr is defined in the __init__ due to its reliance on DB items.

        new_compare : forms.ChoiceField
            Describes the comparison operation between the PV's value and 
            the triggering value (new_value)

        new_name : forms.CharField
            Changes to the trigger name can be entered in this field

        new_value : forms.FloatField
            Changes to the triggering value can be entered in this field

    """
    def __init__(self,*args,**kwargs):
        """Constrct the object
        """
        super().__init__(*args,**kwargs)
        self.fields['new_pv'] = forms.ChoiceField(
            label = 'PV name',
            # use this to sort alphabetiaclly if necessary
            # sorted([(np.random.random(),np.random.random()) for x in range(10)],key=lambda s: s[1])
            #choices = [(-1,None)] + [ (x.pk,x.name) for x in Pv.objects.all()],
            # choices = ["a,"b"],
            widget = forms.HiddenInput(
            )
        )
    

        self.fields['new_compare'] = forms.ChoiceField(
            label = 'Comparison',
            choices = [(-1,None)] + Trigger.compare_choices,
            widget = forms.Select(
                attrs = {
                    'class':'custom-select',
                    }
                )
        )
    
    
    new_name = forms.CharField(
        label = 'Trigger name',
        max_length = Trigger.name_max_length,
        widget = forms.TextInput( 
            attrs = {
                'class':'form-control',
                'type':'text',
            }
        )
    )

    new_value = forms.FloatField(
        label = 'Value',
        required = False,
        widget = forms.NumberInput(
            attrs = {
                'class':'form-control',
            }
        )
    )



    def clean_new_name(self):
        data = self.cleaned_data['new_name']
        # print("DATA:",data)
        # if len(data) <= 0 or data == None:
        #     raise forms.ValidationError(
        #         'Links must have unique anchors and URLs.',
        #         code='duplicate_links'
        #     )
        return data
        '''# data is received as a single sting
        data = self.cleaned_data['new_owners']
        
        # produce list of individual usernames from textbox
        name_list = [name.strip() for name in data.split(",")]
        name_set = set(name_list)
        name_set = name_set - set(['',' '])

        # search database 
        profile_list = Profile.objects.filter(user__username__in=name_set)

        # find lists of accepted and rejected usernames for reporting errors
        user_list = User.objects.filter(profile__in=profile_list)
        accepted_name_list = [ name['username'] for name in user_list.values()]
        rejected_name_set = name_set - set(accepted_name_list)
        if rejected_name_set:
            error_msg = ""
            for rejected_name in rejected_name_set:
                error_msg += (rejected_name + ", ")

            raise forms.ValidationError(
                "Usernames "+error_msg+"Not recognized"
            )'''
    def clean_new_pv(self):
        data = self.cleaned_data['new_pv']
        if data == str(-1):
            data = None
        else:
            data = Pv.objects.get(pk=int(data))

        return data

    def clean_new_compare(self):
        data = self.cleaned_data['new_compare']
        if data == str(-1):
            data = None
        if data == "":
            data = None

        return data


class configAlert(forms.Form):#ModelForm
    """Define the fields for an alert. These are the editable fields that
    presented to users who have ownership over this alert.

    Attributes
    ----------
        new_owners : forms.MultipleChoiceField
            Provides dropdown selection of profiles who can own this object.
            The user can give ownership to themselves and others. This does NOT
            register these users to receive alerts. This attr is defined in 
            the __init__ due to its reliance on DB items.

        new_name : forms.CharField
            Changes to the alert name can be entered in this field.abs

        new_subscribe : forms.BooleanField
            Determines whether the current user is subscribed.             
    """

    class Meta:
        model = Alert

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
            
        try:
            post_request = args[0]
        except IndexError:
            post_request = False


    new_name = forms.CharField(
        label = 'Alert name',
        max_length = Alert.name_max_length,
        widget = forms.TextInput( 
            attrs = {
                'class':'form-control',
                'type':'text',
            }
        ),
        help_text = str(Alert.name_max_length) + " character limit"
    )

    new_subscribe = forms.BooleanField(
        label = "Subscribe",
        required = False,
        widget = HorizontalCheckbox(
            attrs = {
                'class':'form-check-input position-static',
                'type':'checkbox',
            }
        ),
        help_text = 'Check this box to receive alerts',
    )

    new_lockout_duration = forms.DurationField(
        label = "Lockout delay",
        required = False,
        widget = forms.TimeInput(
            attrs = {
                'class':'form-control',
                'type':'text',
                'placeholder':'dd hh:mm:ss',
            }
        ),
        help_text = "Time delay between successive alerts"
    )
    
    new_owners = forms.CharField(
        label = 'Owners',
        strip = True,
        widget = forms.Textarea(
            attrs = {
                'class':'form-control',
                'rows':'5',
            }
        ),
        help_text = "Users who can edit this alert"
    )
    
    def clean_new_owners(self):
        """Receive input string for the new_owners field and return users list

        Returns
        -------
        list of Django.db.models.query.Queryset
            This queryset contains the list of profiles (NOT User objects) to
            have ownership of this Alert.

        """
        # data is received as a single sting
        data = self.cleaned_data['new_owners']
        
        # produce list of individual usernames from textbox
        name_list = [name.strip() for name in data.split(",")]
        name_set = set(name_list)
        name_set = name_set - set(['',' '])

        # search database 
        profile_list = Profile.objects.filter(user__username__in=name_set)

        # find lists of accepted and rejected usernames for reporting errors
        user_list = User.objects.filter(profile__in=profile_list)
        accepted_name_list = [ name['username'] for name in user_list.values()]
        rejected_name_set = name_set - set(accepted_name_list)
        if rejected_name_set:
            error_msg = ""
            for rejected_name in rejected_name_set:
                error_msg += (rejected_name + ", ")

            raise forms.ValidationError(
                "Usernames "+error_msg+"Not recognized"
            )

        return profile_list 

    def clean_new_subscribe(self):
        """Validate the subscription option

        Returns
        -------
        bool
            True if the user has selected the subscriber option

        Note
        ----
            Todo field isn't working? Confirm that this function works with 
            missing fields.
            This field can occasionally report None and is notorious for
            bugging after changes


        """
        
        if self.cleaned_data['new_subscribe']:
            data = True
        else:
            data = False

        return data


class detailAlert(forms.Form):
    """Define the fields for an alert. These fields are presented when the user
    does NOT own this alert. The only option is to subscribe.
    """
    class Meta:
        model = Alert
    
    new_subscribe = forms.BooleanField(
        label = "Subscribe",
        required = False,
        widget = HorizontalCheckbox(
            attrs = {
                'class':'form-check-input position-static',
                'type':'checkbox',
            }
        ),
        help_text = 'Check this box to receive alerts',
    )
    def clean_new_subscribe(self):
        if self.cleaned_data['new_subscribe']:
            data = True
        elif not self.cleaned_data['new_subscribe']:
            data = False

        return data
    
    
class createPv(forms.ModelForm):
    class Meta:
        model = Pv
        fields = ['new_name']

    new_name = forms.CharField(
        label = 'PV name',
        max_length = Pv.name_max_length,
        widget = forms.TextInput( 
            attrs = {
                'class':'form-control',
                'type':'text',
            }
        )
    )
    # forms.ModelForm.Meta.fields.append(new_name)
     

class deleteAlert(forms.Form):
    class Meta:
        model = Alert
        fields = []
        
        
#class EditProfileForm(UserChangeForm):
#    
#    class Meta:
#        model = User 
#        fields = {
#            'username',
#            'email',
#            'password'
#        }
