from django.shortcuts import render


def home(request):
    my_context = {'name': "Иван", "university": "КАИ"}

    return render(request=request,
                  template_name="Forms/index.html",
                  context=my_context)