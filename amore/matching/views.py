from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import ProposeForm

from django.contrib.auth.models import User
from users.models import Profile
from .models import Proposal, Relationship

@login_required
def home(request):

    user = request.user
    profile = Profile.objects.filter(id = user.id)
    proposals = Proposal.objects.filter(user = request.user).count()
    #conquests = profile.conquests.count()

    context = {
        'profile' : profile,
        'user' : user,
        'proposals' : proposals,
        #'conquests' : conquests,
    }

    return render(request, 'matching/home.html', context)

def view_profile(request, pk):

    profile = get_object_or_404(Profile, pk=pk)
    age = profile.get_age()
    context = {
        'profile' : profile,
        'age' : age,
    }

    return render(request, 'matching/profile.html', context)


def propose(request, pk):

    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':

        form = ProposeForm(request.POST)
        if form.is_valid():

            user = request.user
            proposal = Proposal.objects.create(user = request.user, to_user = profile.user)
            proposal.message = form.cleaned_data['message']

            profile.conquests.add(request.user)
            user.profile.proposals.add(proposal)

            user.profile.save()
            profile.save()
            proposal.save()

            return redirect('home')

    return render(request, 'matching/propose.html', {'profile':profile, 'form':form})


def cancel_proposal(request, pk):

    profile = get_object_or_404(Profile, pk=pk)
    user = request.user

    Proposal.objects.filter(user = request.user).delete()
    profile.conquests.remove(request.user)

    user.profile.save()
    profile.save()

    return redirect('find_matches')

@login_required
def decline_proposal(request, pk):

    proposal = get_object_or_404(Proposal, pk=pk)
    proposal.status = 0
    proposal.save()

    return HttpResponseRedirect(proposal.get_absolute_url())

@login_required
def accept_proposal(request, pk):

    proposal = get_object_or_404(Proposal, pk=pk)
    relationship = Relationship.objects.create(proposal = proposal)

    proposal.user.profile.relationships.add(relationship)
    proposal.to_user.profile.relationships.add(relationship)

    proposal.user.profile.status = 1
    proposal.to_user.profile.status = 1
    proposal.status = 1
    relationship.status = 1

    proposal.user.profile.save()
    proposal.to_user.profile.save()
    proposal.save()
    relationship.save()

    return HttpResponseRedirect(relationship.get_absolute_url())

@login_required
def proposal_home(request, pk):

    proposal = get_object_or_404(Proposal, pk=pk)
    context = {
        'proposal' : proposal
    }

    return render(request, 'matching/proposal_home.html', context)

@login_required
def relationship_home(request, pk):

    rel = get_object_or_404(Relationship, pk=pk)
    context = {
        'rel' : rel
    }

    return render(request, 'matching/relationship_home.html', context)

@login_required
def break_up(request, pk):

    relationship = get_object_or_404(Relationship, pk=pk)
    relationship.proposal.user.profile.status = 0
    relationship.proposal.user.profile.breakups += 1

    relationship.proposal.to_user.profile.status = 0
    relationship.proposal.to_user.profile.breakups += 1

    relationship.status = 0

    relationship.proposal.user.profile.save()
    relationship.proposal.to_user.profile.save()
    relationship.proposal.save()
    relationship.save()

    return HttpResponseRedirect('home')

@login_required
def suggest_matches(request):

    user = request.user

    pool = Profile.objects.exclude(sex = user.profile.sex)
    context = {
        'pool' : pool,
    }

    return render(request, 'matching/find_matches.html', context)

@login_required
def conquest_list(request):
    profile = get_object_or_404(Profile, user = request.user)
    proposals = Proposal.objects.filter(to_user=request.user).all()

    return render(request, 'matching/conquests_list.html', {'profile':profile, 'proposals':proposals})

@login_required
def relationship_view(request):

    profile = get_object_or_404(Profile, user=request.user)
    if profile.relationships.filter(status=1).exists():
        rel = profile.relationships.filter(status=1).all()[0]
        return HttpResponseRedirect(rel.get_absolute_url())
    else :
        return redirect('home')

# Create your views here.
