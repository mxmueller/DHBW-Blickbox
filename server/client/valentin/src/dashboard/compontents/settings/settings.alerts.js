import React, { useEffect, useState } from "react";
import { Checkbox } from "@chakra-ui/react";
import Cookies from "js-cookie";

const welcomeMessage = {
  title: "Vielen Dank!",
  body: "Browser Push-Mitteilungen wurden erfolgreich aktiviert. 🥳",
};

const disableMessage = {
  title: "Deaktiviert!",
  body: "Browser Push-Mitteilungen wurden deaktiviert. 😢",
};

function UserSettings() {
  const [isCheckboxChecked, setIsCheckboxChecked] = useState(false);
  const [notificationPermission, setNotificationPermission] =
    useState("default");
  const [isCheckboxEnabled, setIsCheckboxEnabled] = useState(true);
  const [, setIsFirstTime] = useState(true);

  useEffect(() => {
    const notificationEnabled = Cookies.get("notificationEnabled");
    if (notificationEnabled === undefined) {
      Cookies.set("notificationEnabled", false, { expires: 365 }); // Set cookie to expire in 1 year
    } else {
      setIsCheckboxChecked(notificationEnabled === "true");
      setNotificationPermission("granted");
    }
  }, []);

  const handleCheckboxChange = async () => {
    setIsCheckboxEnabled(!isCheckboxEnabled);
    if (!isCheckboxChecked) {
      if ("Notification" in window) {
        const permission = await Notification.requestPermission();
        setNotificationPermission(permission);
        if (permission === "granted") {
          Cookies.set("notificationEnabled", true, { expires: 365 }); // Set the cookie to expire in 1 year
          sendNotification(welcomeMessage.title, welcomeMessage.body);
          setIsFirstTime(false);
        }
      }
    } else {
      Cookies.set("notificationEnabled", false, { expires: 365 }); // Set the cookie to expire in 1 year
      sendNotification(disableMessage.title, disableMessage.body);
    }
    setIsCheckboxChecked(!isCheckboxChecked);
  };

  const sendNotification = (alertTitle, alertBody) => {
    const notificationTitle = alertTitle;
    new Notification(notificationTitle, {
      body: alertBody,
    });
  };

  return (
    <div>
      <Checkbox
        colorScheme="gray"
        isChecked={isCheckboxChecked && notificationPermission === "granted"}
        onChange={handleCheckboxChange}
        disabled={
          notificationPermission !== "default" &&
          notificationPermission !== "granted" &&
          isCheckboxEnabled
        }
      >
        Push-Benachrichtigung erhalten
      </Checkbox>
    </div>
  );
}

export default UserSettings;
