const form = document.getElementById('login-form');

form.addEventListener('submit', async (e) => {
    e.preventDefault(); // ngăn trình duyệt load lại trang

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
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
        alert('Không thể kết nối tới server. Có thể server bị lỗi hoặc bạn đang offline.');
    }
});
