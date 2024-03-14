import Cookies from 'js-cookie';

const sendNotification = (title, body) => {
    const notificationEnabled = Cookies.get('notificationEnabled');
    if (notificationEnabled === 'true') {
        if (
            'Notification' in window &&
            Notification.permission === 'granted'
        ) {
            new Notification(title, { body });
        }
    }
};

export default sendNotification;
