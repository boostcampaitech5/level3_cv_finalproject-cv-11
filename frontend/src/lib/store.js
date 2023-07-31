import { useState, useEffect } from 'react';

const PersistStorage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key);
    const [value, setValue] = useState(
        storedValueStr != null ? JSON.parse(storedValueStr) : initValue
    );

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return {value, setValue};
};

export const page = PersistStorage("page", 0);
export const access_token = PersistStorage("access_token", "");
export const user_name = PersistStorage("username", "");
export const is_login = PersistStorage("is_login", false);