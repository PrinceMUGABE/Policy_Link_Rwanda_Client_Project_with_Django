document.addEventListener('DOMContentLoaded', function() {
    const institutionTypeSelect = document.getElementById('institutionType');
    const institutionSelect = document.getElementById('institution');
    const departmentSelect = document.getElementById('department');
    const policyDisplayArea = document.querySelector('.policy-display');
    const paginationDiv = document.getElementById('pagination');
    const policiesPerPage = 1; // Number of policies to display per page
    let currentPage = 1; // Current page

    institutionTypeSelect.addEventListener('change', function() {
        fetchInstitutions(this.value);
    });

    institutionSelect.addEventListener('change', function() {
        fetchDepartments(this.value);
    });

    departmentSelect.addEventListener('change', function() {
        currentPage = 1; // Reset current page when department changes
        fetchPolicies();
    });

    function fetchInstitutions(type) {
        fetch(`/ajax/get_institutions/?type=${type}`)
            .then(response => response.json())
            .then(data => {
                institutionSelect.innerHTML = '<option value="">Select Institution</option>';
                data.forEach(institute => {
                    institutionSelect.innerHTML += `<option value="${institute.id}">${institute.name}</option>`;
                });
            });
    }

    function fetchDepartments(institutionId) {
        fetch(`/ajax/get_departments/?institution_id=${institutionId}`)
            .then(response => response.json())
            .then(data => {
                departmentSelect.innerHTML = '<option value="">Select Department</option>';
                data.forEach(department => {
                    departmentSelect.innerHTML += `<option value="${department.id}">${department.name}</option>`;
                });
            });
    }

   function fetchPolicies() {
    const departmentId = departmentSelect.value;
    if (!departmentId) {
        // If no department is selected, clear the policy display area
        policyDisplayArea.innerHTML = '';
        return;
    }

    fetch(`/ajax/get_policies/?department_id=${departmentId}`)
        .then(response => response.json())
        .then(data => {
            const policies = data.policies;
            const departmentName = data.department_name;
            const instituteName = data.institute_name;
            const instituteType = data.institute_type;

            // Display selected department and institute information
            document.getElementById('selected-info').innerHTML = `
                <p><strong>Institution:</strong> ${instituteName}</p>
                <p><strong>Institution Type:</strong> ${instituteType}</p>
                <p><strong>Department:</strong> ${departmentName}</p>
            `;

            // Clear previous policies
            policyDisplayArea.innerHTML = '';

            // Display policies
            policies.forEach(policy => {
                const policyDiv = document.createElement('div');
                policyDiv.classList.add('policy');
                policyDiv.innerHTML = `
                    <p><strong>Institution:</strong> ${instituteName}</p>
                    <p><strong>Department:</strong> ${departmentName}</p>
                    <p><strong>Institution Type:</strong> ${instituteType}</p>

                    <p><strong>Policy name:</strong> ${policy.name}</p>
                    <h3><strong>Description</strong></h3>
                    <p>${policy.description}</p>
                    <div class="rating">
                        ${getStarRatingHTML()}
                    </div>
                    <form class="comment-form">
                        <textarea name="comment" placeholder="Write a comment..."></textarea>
                        <button type="submit">Submit</button>
                    </form>
                `;
                policyDisplayArea.appendChild(policyDiv);
            });

            updatePaginationButtons(policies.length);
        })
        .catch(error => {
            console.error('Error fetching policies:', error);
            policyDisplayArea.innerHTML = '<p>Error fetching policies. Please try again later.</p>';
        });
}




    function getStarRatingHTML(rating) {
    let starsHTML = '';
    for (let i = 0; i < 5; i++) {
        if (i < rating) {
            starsHTML += '<span class="star active">&#9733;</span>';
        } else {
            starsHTML += '<span class="star">&#9733;</span>';
        }
    }
    return starsHTML;
}


    function updatePaginationButtons(totalPolicies) {
    const totalPages = Math.ceil(totalPolicies / policiesPerPage);

    paginationDiv.innerHTML = '';
    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        button.classList.add('pagination-button');
        if (i === currentPage) {
            button.classList.add('active');
        }
        button.addEventListener('click', function() {
            currentPage = i;
            fetchPolicies();
        });
        paginationDiv.appendChild(button);
    }
}


    // Add event listener to stars for rating
    policyDisplayArea.addEventListener('click', function(event) {
        if (event.target.classList.contains('star')) {
            const stars = event.target.parentElement.querySelectorAll('.star');
            const clickedIndex = Array.from(stars).indexOf(event.target);
            stars.forEach((star, index) => {
                if (index <= clickedIndex) {
                    star.classList.add('active');
                } else {
                    star.classList.remove('active');
                }
            });
        }
    });
});
