import React, { useState } from 'react';
import { FileUploader } from 'react-drag-drop-files';
import axios from 'axios';
import { Link } from 'react-router-dom';

function ShareFile() {
    const [file, setFile] = useState(null);
    const [passcode, setPasscode] = useState('');
    const [shareableLink, setShareableLink] = useState('');
    const [notification, setNotification] = useState('');

    const handleFileUpload = (file) => {
        setFile(file);
        //setPasscode('1234');
        console.log(file);
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            //formData.append('ttl', "60");

            // Send POST request to the backend API using Axios
            axios
                .post('http://127.0.0.1:8000/api/files/', formData)
                .then((response) => {
                    // Handle a successful response from the server, set passcode to "key" in the response body
                    const data = response.data;

                    // If data is an array, take the first item
                    if (Array.isArray(data)) {
                        const passcode = data[0].key;
                        setPasscode(passcode);
                        // Copy the passcode to the clipboard
                        navigator.clipboard.writeText(passcode).then(() => {
                            // Show a notification
                            showNotification('Copied to clipboard!');
                        });
                    }
                })
                .catch((error) => {
                    // Handle errors here
                    console.error('File upload failed', error);
                });
            const baseUrl = 'http://localhost:3000/download/';
            setShareableLink(baseUrl);
        }
    };

    const showNotification = (message) => {
        setNotification(message);

        // Automatically close the notification after 2 seconds
        setTimeout(() => {
            setNotification('');
        }, 2000);
    };

    return (
        <div className="h-screen flex flex-col items-center justify-center bg-gray-100">
            <div className="border p-6 rounded-lg bg-white shadow-md w-96 relative">
                <Link to="/" className="absolute top-2 right-2 text-gray-600 text-sm hover:text-blue-600">
                    Back
                </Link>
                <h1 className="text-2xl font-bold mb-4">Share a file with others!</h1>
                <FileUploader handleChange={handleFileUpload} name="file" />
                {passcode && (
                    <div className="mt-4">
                        <label className="block text-sm font-medium text-gray-700">
                            Passcode:
                        </label>
                        <div className="text-lg font-bold text-blue-600">{passcode}</div>
                    </div>
                )}
                {shareableLink && (
                    <div className="mt-4">
                        <label className="block text-sm font-medium text-gray-700">
                            Download Here:
                        </label>
                        <a href={shareableLink} className="text-lg font-bold text-blue-600">{shareableLink}</a>
                    </div>
                )}
                {notification && (
                    <div className="mt-4">
                        <div className="bg-blue-100 p-2 text-blue-800 rounded">
                            {notification}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ShareFile;
