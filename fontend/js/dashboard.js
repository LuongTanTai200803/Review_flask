// Lấy token từ localStorage
const token = localStorage.getItem('token');

// Nếu không có token, chuyển về login
check(token)

// Kiểm tra hạn của token
function isTokenExpired(token) {
    if (!token) return true;

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const exp = payload.exp;
        const now = Math.floor(Date.now() / 1000);

        return exp < now;
    } catch (e) {
        console.error('Invalid token:', e);
        return true;
    }
}
function check(token){
    if (isTokenExpired(token)) {
        alert("Phiên đăng nhập đã hết. Vui lòng đăng nhập lại.")
    }
}



// Hàm lấy danh sách task
async function fetchTasks() {
    check(token)
    try {
        const response = await fetch('http://127.0.0.1:5000/task/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();
        console.log('Data from server:', data); // log ra xem

        const taskList = document.getElementById('taskList');
        taskList.innerHTML = ''; // clear taskList trước

        if (response.ok) {
            if (Array.isArray(data.tasks) && data.tasks.length > 0) {
                data.tasks.forEach(task => {
                    const li = document.createElement('li');

                    const description = task.description ?? 'Không có mô tả';
                    const due_date = task.due_date ? new Date(task.due_date) : null;
                    const formattedDueDate = due_date && !isNaN(due_date) ? due_date.toLocaleString() : 'Không có ngày hết hạn';

                    li.innerHTML =`
                        <strong>Title:</strong> ${task.title}<br>
                        <strong>Status:</strong> ${task.status}<br>
                        <strong>Description:</strong> ${description}<br>
                        <strong>Due Date:</strong> ${formattedDueDate}<br>
                        <button onclick="editTask('${task.id}')">Edit</button>
                        <button onclick="deleteTask('${task.id}')">Delete</button>
                        <hr>
                    `;

                    taskList.appendChild(li);
                });
            } else {
                // Không có task
                const li = document.createElement('li');
                li.textContent = 'Không có task nào';
                taskList.appendChild(li);
            }
        } else {
            console.error('Response status:', response.status); // thêm dòng này
            console.error('Response data:', data); // thêm dòng này
            alert('Failed to load tasks');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Không thể tải task!');
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

    const defaultTitle = title || "Default Title";  // Nếu title không có, dùng "Default Title"
    const defaultStatus = status || "Pending";     // Nếu status không có, dùng "Pending"
    const defaultDueDate = due_date || null;       // Nếu due_date không có, có thể là null
    const defaultDescription = description || "";  // Nếu description không có, có thể để trống
    check(token)
    try {
            const response = await fetch('http://127.0.0.1:5000/task/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    title: defaultTitle,
                    status: defaultStatus,
                    due_date: defaultDueDate,
                    description: defaultDescription
                })
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = 'dashboard.html';   // chuyển trang
            } else {
                console.error('Response status:', response.status); 
                console.error('Response data:', data); 
                alert(data.msg || data.message || 'Login failed ');
            }
    } catch (error) {
        console.error('Error:', error);
        alert('Không thể tạo task mới!');
    }
});    


// Hàm sửa task
async function editTask(taskId) {
    check(token)
    const confirmDelete = confirm('Bạn có chắc muốn chỉnh sửa task này?');
    if (!confirmDelete) return;
    // Lấy giá trị từ client
    const title = document.getElementById('title').value;
    const status = document.getElementById('status').value;
    const due_date = document.getElementById('due_date').value;
    const description = document.getElementById('description').value;

    const taskData = {};

    // Chỉ thêm vào nếu có giá trị
    if (title) taskData.title = title;
    if (status) taskData.status = status;
    if (due_date) taskData.due_date = due_date;
    if (description) taskData.description = description;

    try {
        const response = await fetch(`http://127.0.0.1:5000/task/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(taskData)
    
        });

        if (response.ok) {
            alert('Task đã được sửa');
            fetchTasks(); // Cập nhật lại danh sách task
        } else {
            const data = await response.json();
            console.error('Error:', data);
            alert('Không thể sửa task');
        }
    } catch (error) {
        console.error('Error:', error);
        console.error('Response data:', data); 
        alert('Không thể kết nối tới server để xóa task');
    }
}

// Hàm xóa task
async function deleteTask(taskId) {
    check(token)
    const confirmDelete = confirm('Bạn có chắc muốn xóa task này?');
    if (!confirmDelete) return;

    try {
        const response = await fetch(`http://127.0.0.1:5000/task/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            alert('Task đã được xóa');
            fetchTasks(); // Cập nhật lại danh sách task
        } else {
            const data = await response.json();
            console.error('Error:', data);
            alert('Không thể xóa task');
        }
    } catch (error) {
        console.error('Error:', error);
        console.error('Response data:', data); 
        alert('Không thể kết nối tới server để xóa task');
    }
}



// Xử lý logout
const logoutButton = document.getElementById('logoutButton');
logoutButton.addEventListener('click', () => {
    localStorage.removeItem('token'); // Xóa token
    window.location.href = 'login.html'; // Chuyển về login
});
