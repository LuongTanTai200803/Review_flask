// Lấy token từ localStorage
const token = localStorage.getItem('token');

// Nếu không có token, chuyển về login
if (!token) {
    window.location.href = 'login.html';
}


// Hàm lấy danh sách task
async function fetchTasks() {
    try {
        const response = await fetch('https://reviewflask-secredkey.up.railway.app/task/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            const taskList = document.getElementById('taskList');
            data.tasks.forEach(task => {
                const li = document.createElement('li');
                li.textContent = task.title;
                taskList.appendChild(li);
            });
        } else {
            alert('Failed to load tasks');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong!');
    }
}

// Gọi hàm fetchTasks() khi vào trang
fetchTasks();

// Xử lý submit form để tạo task mới
const taskForm = document.getElementById('create_task');
taskForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Không cho reload trang

    const title = document.getElementById('title').value;
    const status = document.getElementById('status').value;
    const due_date = document.getElementById('due_date').value;
    const description = document.getElementById('description').value;

    try {
            const response = await fetch('https://reviewflask-secredkey.up.railway.app/task/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    title,
                    status,
                    due_date,
                    description
                })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.access_token); // lưu token
                window.location.href = 'dashboard.html';   // chuyển trang
            } else {
                console.error('Response status:', response.status); // thêm dòng này
                console.error('Response data:', data); // thêm dòng này
                alert(data.msg || data.message || 'Login failed ');
            }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong!');
    }
});    

// Xử lý logout
const logoutButton = document.getElementById('logoutButton');
logoutButton.addEventListener('click', () => {
    localStorage.removeItem('token'); // Xóa token
    window.location.href = 'login.html'; // Chuyển về login
});
