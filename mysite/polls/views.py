from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Person, Guest_list


class IndexView(generic.ListView):
    template_name = 'partyICT4D/index.html'
    context_object_name = 'person_list'

    def get_queryset(self):
        return Guest_list.objects.order_by('-pub_date')[:5]

    def get_queryset(self):
        return Guest_list.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Guest_list
    template_name = 'partyICT4D/detail.html'

    def get_queryset(self):
        return Guest_list.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Guest_list
    template_name = 'partyICT4D/results.html'


def add_people_to_list(request, person_id):
    person = get_object_or_404(Guest_list, pk=person_id)
    try:
        person_list = person.name.get(pk=request.POST['guest_list'])
    except (KeyError, Person.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'partyICT4D/detail.html', {
            # 'question': question,
            'error_message': "You didn't fill in your name",
        })
    else:
        person_list.append(person)
        person_list.save()
        return HttpResponseRedirect(reverse('partyICT4D:results', args=(person.id,)))






# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         return Question.objects.order_by('-pub_date')[:5]
#
#     def get_queryset(self):
#         return Question.objects.filter(
#             pub_date__lte=timezone.now()
#         ).order_by('-pub_date')[:5]
#
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
#
#     def get_queryset(self):
#         return Question.objects.filter(pub_date__lte=timezone.now())
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
#


# class QuestionDetailViewTests(TestCase):
#     def test_future_question(self):
#         future_question = create_question(question_text='Future question.', days=5)
#         url = reverse('polls:detail', args=(future_question.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)
#
#     def test_past_question(self):
#         past_question = create_question(question_text='Past Question.', days=-5)
#         url = reverse('polls:detail', args=(past_question.id,))
#         response = self.client.get(url)
#         self.assertContains(response, past_question.question_text)
