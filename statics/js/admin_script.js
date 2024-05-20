$(document).ready(function() {
    // Toggle sidebar when hamburger menu is clicked
    $('.hamburger-menu').click(function() {
        $('#sidebar').toggleClass('active');
    });

    // Function to fetch users from the backend
    function fetchUsers() {
        $.ajax({
            url: "{% url 'view_all_users' %}", // URL to fetch users
            method: "GET",
            success: function (data) {
                // Render users in the user list section
                $("#user-list").html(data);
            },
            error: function (xhr, status, error) {
                console.error("Error fetching users:", error);
            }
        });
    }
});

function editUser(userId) {
    $.ajax({
        url: '/user_edit/?user_id=' + userId,
        method: 'GET',
        success: function(data) {
            // Populate the edit user form fields with the user's data
            $('#username').val(data.username);
            $('#email').val(data.email);
            $('#phone').val(data.phone);
            $('#role').val(data.role);
        },
        error: function(xhr, status, error) {
            console.error('Error fetching user data:', error);
        }
    });
}


 // Function to handle user deletion via AJAX
        $(".delete-link").click(function() {
            var userId = $(this).data("userid"); // Get the user ID from data attribute
            // Send AJAX request to delete user
            $.ajax({
                url: "{% url 'delete_user' %}",
                type: "POST",
                data: {
                    'user_id': userId,
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                success: function(data) {
                    // Remove the deleted user row from the table
                    $("#user-" + userId).remove();
                },
                error: function(xhr, status, error) {
                    console.error(xhr.responseText);
                }
            });
        });
