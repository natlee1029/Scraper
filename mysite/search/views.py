import json
import traceback
import sys
import csv
import os

from functools import reduce
from operator import and_

from django.shortcuts import render
from django import forms

from summer import find_listings

NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
    dept='Department',
    course_num='Course',
    section_num='Section',
    day='Day',
    time_start='Time (start)',
    time_end='Time (end)',
    enroll='Enrollment',
)


def _valid_result(res):
    """Validate results returned by find_courses."""
    (HEADER, RESULTS) = [0, 1]
    ok = (isinstance(res, (tuple, list)) and
          len(res) == 2 and
          isinstance(res[HEADER], (tuple, list)) and
          isinstance(res[RESULTS], (tuple, list)))
    if not ok:
        return False

    n = len(res[HEADER])

    def _valid_row(row):
        return isinstance(row, (tuple, list)) and len(row) == n
    return reduce(and_, (_valid_row(x) for x in res[RESULTS]), True)


def _load_column(filename, col=0):
    """Load single column from csv file."""
    with open(filename) as f:
        col = list(zip(*csv.reader(f)))[0]
        return list(col)


def _load_res_column(filename, col=0):
    """Load column from resource directory."""
    return _load_column(os.path.join(RES_DIR, filename), col=col)


def _build_dropdown(options):
    """Convert a list to (value, caption) tuples."""
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]

LOCATION = _build_dropdown([None] + _load_res_column('location.csv')) #add appropriate csv file in the string later
SUBJECT = _build_dropdown([None] + _load_res_column('subject.csv')) #add appropriate csv file in the string later

class IntegerRange(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.IntegerField(),
                  forms.IntegerField())
        super(IntegerRange, self).__init__(fields=fields,
                                           *args, **kwargs)

    def compress(self, data_list):
        if data_list and (data_list[0] is None or data_list[1] is None):
            raise forms.ValidationError('Must specify both lower and upper '
                                        'bound, or leave both blank.')

        return data_list


class FloatRange(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.FloatField(),
                  forms.FloatField())
        super(IntegerRange, self).__init__(fields=fields,
                                           *args, **kwargs)

    def compress(self, data_list):
        if data_list and (data_list[0] is None or data_list[1] is None):
            raise forms.ValidationError('Must specify both lower and upper '
                                        'bound, or leave both blank.')

        return data_list        


class CostRange(FloatRange):
    def compress(self, data_list):
        super(EnrollmentRange, self).compress(data_list)
        for v in data_list:
            if not 1 <= v <= 20000:
                raise forms.ValidationError(
                    'Costs must be in the range 1 to 20000.')
        if data_list and (data_list[1] < data_list[0]):
            raise forms.ValidationError(
                'Lower bound must not exceed upper bound.')
        return data_list


class AgeRange(IntegerRange):
    def compress(self, data_list):
        super(TimeRange, self).compress(data_list)
        for v in data_list:
            if not 1 <= v <= 21:
                raise forms.ValidationError(
                    'Ages must be in the range 1 to 21.')
        if data_list and (data_list[1] < data_list[0]):
            raise forms.ValidationError(
                'Lower bound must not exceed upper bound.')
        return data_list


class DateRange(IntegerRange):
    def compress(self, data_list):
        super(TimeRange, self).compress(data_list)
        for v in data_list:
            if not 1 <= v <= 21:
                raise forms.ValidationError(
                    'Ages must be in the range 1 to 21.')
        if data_list and (data_list[1] < data_list[0]):
            raise forms.ValidationError(
                'Lower bound must not exceed upper bound.')
        return data_list


RANGE_WIDGET = forms.widgets.MultiWidget(widgets=(forms.widgets.NumberInput,
                                                  forms.widgets.NumberInput))


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search terms',
        help_text='e.g. science',
        required=False)
    cost = CostRange(
        label='Cost (lower/upper)',
        help_text='e.g. 500 and 3000',
        widget=RANGE_WIDGET,
        required=False)
    age = AgeRange(
        label='Age (lower/upper)',
        help_text='e.g. 12-15',
        widget=RANGE_WIDGET,
        required=False)
    
    location = forms.ChoiceField(label = "Location", choices = LOCATION, required = False)
    subject = forms.ChoiceField(label = "Subject", choices = SUBJECT, required = False)


def home(request):
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():

            # Convert form data to an args dictionary for find_courses
            args = {}
            if form.cleaned_data['query']:
                args['terms'] = form.cleaned_data['query']
            cost = form.cleaned_data['cost']
            if cost:
                args['cost_lower'] = cost[0]
                args['cost_upper'] = cost[1]
            age = form.cleaned_data['age']
            if age:
                args['age_lower'] = age[0]
                args['age_upper'] = age[1]

            duration = form.cleaned_data['duration'] #change based on the dictionary input columns
            if duration:
                args['duration'] = duration
            
            location = form.cleaned_data['location']
            if location:
                args['location'] = location

            subject = form.cleaned_data['subject']
            if subject:
                args['subject'] = subject


            try:
                res = find_courses(args)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in find_listings:
                <pre>{}
{}</pre>
                """.format(e, '\n'.join(bt))

                res = None
    else:
        form = SearchForm()

    # Handle different responses of res
    if res is None:
        context['result'] = None
    elif isinstance(res, str):
        context['result'] = None
        context['err'] = res
        result = None
    elif not _valid_result(res):
        context['result'] = None
        context['err'] = ('Return of find_courses has the wrong data type. '
                          'Should be a tuple of length 4 with one string and '
                          'three lists.')
    else:
        columns, result = res

        # Wrap in tuple if result is not already
        if result and isinstance(result[0], str):
            result = [(r,) for r in result]

        context['result'] = result
        context['num_results'] = len(result)
        context['columns'] = [COLUMN_NAMES.get(col, col) for col in columns]

    context['form'] = form
    return render(request, 'index.html', context)
