document.addEventListener('DOMContentLoaded', () => {
    const loginScreen = document.getElementById('login-screen');
    const chatScreen = document.getElementById('chat-screen');
    const loginForm = document.getElementById('login-form');
    const nicknameInput = document.getElementById('nickname');
    const passwordInput = document.getElementById('password');
    const errorMsg = document.getElementById('login-error');
    const registerBtn = document.getElementById('register-btn');

    let currentUser = null;

    //переключение экранов
    function showChatScreen() {
        loginScreen.classList.remove('active');
        loginScreen.classList.add('hidden');

        chatScreen.classList.remove('hidden');
        chatScreen.classList.add('active');
    }

    //кнопка войти
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorMsg.classList.add('hidden');

        const nickname = nicknameInput.value;
        const password = passwordInput.value;
        const user = await loginUserAPI(nickname, password);

        if (user) {
            currentUser = user;
            console.log("Успешный вход:", currentUser);
            showChatScreen();
        } else {
            errorMsg.textContent = "Неверный логин или пароль";
            errorMsg.classList.remove('hidden');
        }
    });

    //кнопка зарегаться
    registerBtn.addEventListener('click', async () => {
        errorMsg.classList.add('hidden');

        const nickname = nicknameInput.value;
        const password = passwordInput.value;

        if (nickname.length < 3 || password.length < 3) {
            errorMsg.textContent = "Ник и пароль должны быть от 3 символов";
            errorMsg.classList.remove('hidden');
            return;
        }

        const newUser = await registerUserAPI(nickname, password);

        if (newUser) {
            currentUser = newUser;
            console.log("Успешно зарегались:", currentUser);
            showChatScreen();
        } else {
            errorMsg.textContent = "Ошибка регистрации";
            errorMsg.classList.remove('hidden');
        }
    });
});

//ЛОГИКА ПРОФИЛЯ
const profileModal = document.getElementById('profile-modal');
const myProfileTrigger = document.getElementById('my-profile-trigger');
const closeProfileBtn = document.getElementById('close-profile-btn');

//открыть профиль
if (myProfileTrigger) {
    myProfileTrigger.addEventListener('click', () => {
        profileModal.classList.remove('hidden');
    });
}

//по крестику
if (closeProfileBtn) {
    closeProfileBtn.addEventListener('click', () => {
        profileModal.classList.add('hidden');
    });
}

//закрыть при клике
profileModal.addEventListener('click', (e) => {
    if (e.target === profileModal) {
        profileModal.classList.add('hidden');
    }
});