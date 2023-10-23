import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function DownloadFile() {
    const [passcode, setPasscode] = useState('');
    const [fileData, setFileData] = useState(null);

    const handlePasscodeChange = (e) => {
        setPasscode(e.target.value);
    };

    const handleDownloadFile = () => {
        if (passcode) {
            // Send an API request to your backend with the passcode
            axios.get(`http://127.0.0.1:8000/api/files/${passcode}`, { responseType: 'blob' })
                .then((response) => {
                    // Create a blob from the response data
                    const blob = new Blob([response.data], { type: response.headers['content-type'] });

                    // Create a URL for the blob
                    const url = window.URL.createObjectURL(blob);

                    // Create a temporary anchor element for downloading the file
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'downloaded-file.txt'; // Specify the filename
                    a.click();

                    // Revoke the URL to release resources
                    window.URL.revokeObjectURL(url);
                })
                .catch((error) => {
                    // Handle errors, e.g., show an error message
                    console.error('File download failed', error);
                });
        } else {
            // Handle the case when passcode is null or empty
            console.error('Passcode is required.');
            // You can show an error message or take other actions as needed.
        }
    };

    return (
        <div className="h-screen flex flex-col items-center justify-center bg-gray-100">
            <div className="border p-6 rounded-lg bg-white shadow-md w-96 relative">
                <Link to="/" className="absolute top-2 right-2 text-gray-600 text-sm hover:text-blue-600">
                    Back
                </Link>
                <h1 className="text-2xl font-bold mb-4">Download File</h1>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Enter Passcode:
                    </label>
                    <input
                        type="text"
                        value={passcode}
                        onChange={handlePasscodeChange}
                        className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300"
                    />
                </div>
                <button onClick={handleDownloadFile} className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg w-full">
                    Download File
                </button>
            </div>
        </div>
    );
}

export default DownloadFile;
