# pylint: disable=C0114, E5142, C0116, C0411
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from messaging.models import Message
from messaging.forms import MessageForm


@login_required(login_url='/login/')
def inbox(request):
    if (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Message.objects.filter(id=id).delete()
        return redirect("/inbox/")
    incoming = Message.objects.filter(receiver=request.user)
    outgoing = Message.objects.filter(sender=request.user)
    context = {
        "incoming": incoming,
        "outgoing": outgoing
    }
    return render(request, 'messaging/inbox.html', context)

@login_required(login_url='/login/')
def compose(request):
    if request.method == "POST":
        if "add" in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                newMsg = form.save(commit=False)
                newMsg.sender = request.user
                try:
                    newMsg.receiver = User.objects.get(username=form.cleaned_data["recipient"])
                except User.DoesNotExist:
                    context = {
                        "form_data": form,
                        "dne": form.cleaned_data["recipient"],
                    }
                    return render(request, "messaging/compose.html", context)
                newMsg.save()
                return redirect("/inbox/")
            context = {
                "form_data": form
            }
            return render(request, "messaging/compose.html", context)
        return redirect("/inbox/")
    context = {
        "form_data": MessageForm()
    }
    return render(request, "messaging/compose.html", context)
