const API_URL = 'http://localhost:8000';

//регистрация
async function registerUserAPI(nickname, password) {
    try {
        const response = await fetch(`${API_URL}/users/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({
                username: nickname,
                password: password,
                display_name: nickname
            })
        });

        if (response.ok) {
            const userData = await response.json();
            return userData;
        } else {
            return null;
        }
    } catch (error) {
        console.error("Ошибка сети:", error);
        return null;
    }
}

//логин
async function loginUserAPI(nickname, password) {
    // потом
    return { id: 1, username: nickname, display_name: nickname };
}