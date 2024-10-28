from django.shortcuts import render, redirect
from .models import FriendRequest, Friend
from users.models import Profile
from django.db.models import Q
from django.urls import reverse


def connect_with_friends(request):    
    user_profile = request.user.profile  # Ensure this is a Profile instance
    profiles = Profile.objects.exclude(user=request.user)  # Exclude by User instance

    # Now it contains the querysets of Friends in which user is present
    friends_relationships = Friend.objects.filter(Q(user1=user_profile) | Q(user2=user_profile))

    # It extracts users profiles who are friends
    friends_profiles = []
    for relationship in friends_relationships:
        if relationship.user1 == user_profile:
            friends_profiles.append(relationship.user2) 
        else:
            friends_profiles.append(relationship.user1) 

    # Extract friends requests list
    friend_requests = FriendRequest.objects.filter(to_user=user_profile, accepted=False)

    # Extract Person fr sent already
    sent_requests = FriendRequest.objects.filter(from_user=user_profile, accepted=False)

    # Accepted Friend Requests 
    accepted_requests = FriendRequest.objects.filter(from_user=user_profile, accepted=True)

    if request.method == "POST":
        if 'send_request' in request.POST:
            to_user_id = request.POST.get('to_user_id')
            to_user_profile = Profile.objects.get(id=to_user_id)
            new_friend_request = FriendRequest.objects.create(from_user=user_profile, to_user=to_user_profile)
            # Redirect to the same view after sending the request
            return redirect('connect_with_friends')    # Ensure this matches your URL name
        
        if 'accept_request' in request.POST:
            request_id = request.POST.get('request_id')
            friend_request = FriendRequest.objects.get(id=request_id)
            friend_request.accepted = True
            friend_request.save()

            user_profile.followers.add(friend_request.from_user.user)
            accepted_user_profile = friend_request.from_user
            accepted_user_profile.following.add(user_profile.user)

            # Check if the corresponding friend request exists for the accepted user
            reciprocal_request = FriendRequest.objects.filter(
                from_user=friend_request.to_user,
                to_user=friend_request.from_user,
                accepted=True
            ).first()

            # If reciprocal request exists, add both profiles to the Friends model
            if reciprocal_request:
                Friend.objects.create(user1=user_profile, user2=accepted_user_profile)
                friends_profiles.append(accepted_user_profile)

            # Redirect to the same view after accepting the request
            return redirect('connect_with_friends')  # Ensure this matches your URL name
        
        if 'delete_request' in request.POST:
            request_id = request.POST.get('request_id')
            try:
                # Retrieve the friend request and delete it
                friend_request = FriendRequest.objects.get(id=request_id)
                friend_request.delete()  # Delete the request
            except FriendRequest.DoesNotExist:
                # Handle the case where the request does not exist
                pass  
            # Redirect to the same view after deleting the request
            return redirect('connect_with_friends')  # Ensure this matches your URL name

    # Add the context data here for both GET and POST requests
    context = {
        'profiles': profiles,
        'friends_profiles': friends_profiles,
        'friend_requests': friend_requests,
        'sent_requests': sent_requests,
        'accepted_requests': accepted_requests,
    }

    # Return the rendered template for GET requests
    return render(request, 'connect/friends.html', context)
