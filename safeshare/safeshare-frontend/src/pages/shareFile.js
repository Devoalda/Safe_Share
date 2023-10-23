import React, { useState } from 'react';
import { FileUploader } from 'react-drag-drop-files';
import axios from 'axios';
import { Link } from 'react-router-dom';

function ShareFile() {
    const [file, setFile] = useState(null);
    const [passcode, setPasscode] = useState('');

    const handleFileUpload = (file) => {
        setFile(file);
        //setPasscode('1234');
        console.log(file);
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            //formData.append('ttl', "60");

            // Send POST request to the backend API using Axios
            axios.post('http://127.0.0.1:8000/api/files/', formData)
                .then(response => {
                    // Handle a successful response from the server, set passcode to "key" in the response body
                    const data = response.data;

                    // If data is an array, take the first item
                    if (Array.isArray(data)) {
                        setPasscode(data[0].key);
                    }
                })
                .catch(error => {
                    // Handle errors here
                    console.error('File upload failed', error);
                });
        }
    };

    // return (
    //     <div className="h-screen flex flex-col items-center justify-center bg-gray-100">
    //         <div className="border p-6 rounded-lg bg-white shadow-md w-96">
    //             <h1 className="text-2xl font-bold mb-4">Safe-Share</h1>
    //             <label className="block text-sm font-medium text-gray-700 mb-2">
    //                 Upload a File
    //             </label>
    //             <FileUploader handleChange={handleFileUpload} name="file" />
    //             {passcode && (
    //                 <div className="mt-4">
    //                     <label className="block text-sm font-medium text-gray-700">
    //                         Passcode:
    //                     </label>
    //                     <div className="text-lg font-bold text-blue-600">{passcode}</div>
    //                 </div>
    //             )}
    //         </div>
    //     </div>
    // );
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
            </div>
        </div>
    );
}

export default ShareFile;
