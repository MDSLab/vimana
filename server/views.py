from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect,Http404

from .test_api import api_call



def main(request,id=None):

    context={
    }
    return render(request,"main.html",context)


def test(request):
    input_file  = request.POST.get('file')
    # image = request.FILES['trainImage']
    # print(image)
    result = api_call(input_file)
    print(input_file)
    print("--------RESULT-------------")
    print(result)
 
    return HttpResponse(result)