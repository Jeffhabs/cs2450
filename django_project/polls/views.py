from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, ListView, View
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from .models import Choice, Question


class ChoiceVoteView(View):
    def get(self, *args, **kwargs):
        try:
            choice = Choice.objects.get(pk=self.kwargs.get('pk'))
            if choice.question.active:
                choice.votes = choice.votes + 1 if self.kwargs.get('vote') == "up" else choice.votes - 1
                choice.save()
                return HttpResponse(choice.votes, status=200)
            else:
                return HttpResponse("Inactive Question", status=403)
        except:
            return HttpResponse(status=500)


class QuestionList(ListView):
    model = Question
    ordering = ('-pub_date', )


class QuestionDetailView(DetailView):
    model = Question

    def get_queryset(self, *args, **kwargs):
        return Question.objects.filter(pk=self.kwargs.get('pk'))


class QuestionCreateView(CreateView):
    model = Question
    fields = ('question_text',)
    success_url = "/"

    def get_form(self, form_class=None):
        """
        Adds a Crispy Forms helper to the form.
        """
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        form.helper = FormHelper()
        form.helper.form_class = 'form-horizontal'
        form.helper.label_class = 'col-lg-2'
        form.helper.field_class = 'col-lg-8'
        return form

    def form_valid(self, form):
        question = form.save(commit=False)
        question.user = self.request.user
        question.active = True
        return super(QuestionCreateView, self).form_valid(form)


class QuestionCloseView(View):
    def post(self, request, *args, **kwargs):
        print request.user
        if request.user.is_authenticated():
            q = Question.objects.get(pk=self.kwargs.get('pk', None))
            if q.active and request.user == q.user:
                q.active = False
                q.save()
                return HttpResponse(status=200)
        return HttpResponse(status=403)


class ChoiceCreateView(CreateView):
    model = Choice
    fields = ('choice_text',)

    def form_valid(self, form):
        question = Question.objects.get(pk=self.kwargs.get('pk'))
        if question.active:
            choice = form.save(commit=False)
            choice.question = question
            return super(ChoiceCreateView, self).form_valid(form)
        return HttpResponse(status=403)

    def get_success_url(self, *args, **kwargs):
        return reverse('question-detail', kwargs={'pk': self.kwargs.get('pk')})
