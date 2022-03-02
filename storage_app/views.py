from django.shortcuts import render
from django.views import View
from .models import *

class ManualView(View):
    def get(self, request):
        manuals = Manual.objects.all()
        return render(request, "storage_app/index.html", {"manuals": manuals})


class ManualDetailView(View):
    def get(self, request, pk):
        storages = Manual.objects.get(id=pk).storage.all()
        return render(request, "storage_app/manual_detail.html", {"storages": storages})
