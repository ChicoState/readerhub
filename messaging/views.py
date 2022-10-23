from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from messaging.models import Message
from messaging.forms import MessageForm

# Create your views here.

@login_required(login_url='/login/')
def inbox(request):
    if (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Message.objects.filter(id=id).delete()
        return redirect("/inbox/")
    else:
        incoming = Message.objects.filter(receiver=request.user)
        context = {
            "incoming": incoming,
        }
    return render(request, 'messaging/inbox.html', context)