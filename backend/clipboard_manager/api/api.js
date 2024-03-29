// api.js
export const fetchShortcuts = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/shortcuts/');
    if (!response.ok) throw new Error('Network response was not ok');
    return await response.json();
  } catch (error) {
    console.error('There has been a problem with your fetch operation:', error);
  }
};
