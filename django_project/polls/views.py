from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView, DetailView, ListView, View
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
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
    template_name = "polls/question_list.html"

    def get_queryset(self, *args, **kwargs):
        return Question.objects.filter(private=False).order_by('-pub_date')

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionList, self).get_context_data(*args, **kwargs)
        context['heading'] = "All Questions"
        return context


class MyQuestionList(ListView):
    template_name = "polls/question_list.html"

    def get_queryset(self, *args, **kwargs):
        return Question.objects.filter(user=self.request.user).order_by('-pub_date')

    def get_context_data(self, *args, **kwargs):
        context = super(MyQuestionList, self).get_context_data(*args, **kwargs)
        context['heading'] = "My Questions"
        return context


class AuthorQuestionList(ListView):
    template_name = "polls/question_list.html"

    def get_queryset(self, *args, **kwargs):
        return get_list_or_404(
            Question,
            user__username=self.kwargs.get('username', None),
            private=False
        ).order_by('-pub_date')

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorQuestionList, self).get_context_data(*args, **kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username', None))
        context['heading'] = "All Questions by {0}".format(user.username)
        return context


class QuestionDetailView(DetailView):
    model = Question

    def get_template_names(self, *args, **kwargs):
        if self.get_object().private and not self.kwargs.get('uuid'):
            return ["polls/question_private.html"]
        return ["polls/question_detail.html"]

    def get_object(self, queryset=None):
        if self.kwargs.get('uuid', None):
            return Question.objects.get(uuid=self.kwargs.get('uuid'))
        return Question.objects.get(pk=self.kwargs.get('pk', None))


class QuestionCreateView(CreateView):
    model = Question
    fields = ('question_text', 'private')
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


class QuestionUpdatePrivateView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            q = Question.objects.get(pk=self.kwargs.get('pk', None))
            if q.active and request.user == q.user:
                q.private = not q.private
                q.save()
                if q.private:
                    redirect = reverse('question-private', q.get_uuid())
                else:
                    redirect = reverse('question-detail', q.pk)
                return JsonResponse({'redirect': redirect}, status=200)
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
