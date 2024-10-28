document.addEventListener('DOMContentLoaded', function() {
    // Like button functionality
    document.querySelectorAll('.like-button').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            let postId = button.getAttribute('data-post-id');
            let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            // Use fetch instead of jQuery's $.ajax
            fetch("{% url 'home' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: new URLSearchParams({
                    'post_id': postId,
                    'csrfmiddlewaretoken': csrfToken
                })
            })
            .then(response => response.json())
            .then(data => {
                // Update the like count and button text
                button.parentElement.querySelector('.likes-count').textContent = data.likes_count;
                button.innerHTML = '<i class="fas fa-thumbs-up"></i> ' + (data.liked ? 'Unlike' : 'Like');
            })
            .catch(() => {
                alert("An error occurred while liking the post. Please try again.");
            });
        });
    });

    // Comment toggle functionality
    document.querySelectorAll('.comment-toggle-button').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            let postId = button.getAttribute('data-post-id');
            let commentsSection = document.getElementById('comments-section-' + postId);
            commentsSection.style.display = commentsSection.style.display === 'none' ? 'block' : 'none';
        });
    });

    // Add comment functionality
    document.querySelectorAll('.add-comment-button').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            let postId = button.getAttribute('data-post-id');
            let commentContent = button.previousElementSibling.value;
            let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            if (commentContent.trim()) {
                // Use fetch instead of jQuery's $.ajax
                fetch("{% url 'home' %}", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': csrfToken
                    },
                    body: new URLSearchParams({
                        'post_id': postId,
                        'comment_content': commentContent,
                        'csrfmiddlewaretoken': csrfToken
                    })
                })
                .then(response => response.json())
                .then(data => {
                    let newComment = `<p><strong>${data.username}:</strong> ${data.content} <small>Posted on ${data.created_at}</small></p>`;
                    button.closest('.comments').querySelector('.comments-list').insertAdjacentHTML('beforeend', newComment);
                    button.previousElementSibling.value = "";  // Clear the input field
                })
                .catch(() => {
                    alert("An error occurred while adding the comment. Please try again.");
                });
            } else {
                alert("Please enter a comment before submitting.");
            }
        });
    });
});
