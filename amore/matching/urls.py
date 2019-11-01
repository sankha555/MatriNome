from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import (
                    view_profile, suggest_matches, home, break_up,
                    accept_proposal, propose, proposal_home,
                    relationship_home, decline_proposal, cancel_proposal,
                    conquest_list, relationship_view,

                )


urlpatterns = [
    path('', home, name='home'),
    path('user_profile/<int:pk>/', view_profile, name='view_profile'),
    path('find_matches/', suggest_matches, name='find_matches'),
    path('relationship/<int:pk>/', relationship_home, name='relationship_home'),
    path('proposal/<int:pk>/', proposal_home, name='proposal_home'),
    path('proposal/<int:pk>/accepted', accept_proposal, name='accept_proposal'),
    path('proposal/<int:pk>/declined', decline_proposal, name='decline_proposal'),
    path('relationship/<int:pk>/broke_up/', break_up, name='break_up'),
    path('profile/<int:pk>/propose/', propose, name='propose'),
    path('profile/<int:pk>/cancel_propose/', cancel_proposal, name='cancel_proposal'),
    path('my_conquests/', conquest_list, name='conquest_list'),
    path('my_relationship/', relationship_view, name='relationship_view'),
]
