import React, { useState } from 'react';
import { FileUploader } from 'react-drag-drop-files';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Modal from 'react-modal';

const customStyles = {
    content: {
        top: '50%',
        left: '50%',
        right: 'auto',
        bottom: 'auto',
        marginRight: '-50%',
        transform: 'translate(-50%, -50%)',
    },
};
function ShareFile() {
    const [file, setFile] = useState(null);
    const [passcode, setPasscode] = useState('');
    const [ttl, setTtl] = useState('');
    const [shareableLink, setShareableLink] = useState('');
    const [notification, setNotification] = useState('');
    const [errorMsg, setErrorcode] = useState('');
    let subtitle;
    const [modalIsOpen, setIsOpen] = React.useState(false);
    const apiUrl = process.env.REACT_APP_API_HOST || 'localhost:8000';
    console.log(apiUrl);
    // const apiPort = process.env.REACT_APP_API_PORT || '8000';
    //
    // const apiUrl = `${apiHost}:${apiPort}`;

    function openModal() {
        setIsOpen(true);
    }

    function afterOpenModal() {
        // references are now sync'd and can be accessed.
        subtitle.style.color = '#f00';
    }

    function closeModal() {
        setIsOpen(false);
    }

    const handleFileUpload = (file) => {
        setFile(file);
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('ttl', ttl * 24 * 60 * 60);

            // Send POST request to the backend API using Axios
            axios
                .post(`${apiUrl}/api/files/`, formData)
                .then((response) => {
                    // Handle a successful response from the server, set passcode to "key" in the response body
                    const data = response.data;

                    // If data is an array, take the first item
                    if (Array.isArray(data)) {
                        const passcode = data[0].key;
                        const baseUrl = apiUrl + '/api/files/';

                        setPasscode(passcode);
                        setShareableLink(baseUrl + passcode);
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
                    openModal();
                    setErrorcode(error.response.data.msg);
                });
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
            <div>
                <Modal
                    isOpen={modalIsOpen}
                    onAfterOpen={afterOpenModal}
                    onRequestClose={closeModal}
                    style={customStyles}
                    contentLabel="Error Modal"
                    ariaHideApp={false}
                >
                    <h2 ref={(_subtitle) => (subtitle = _subtitle)}>Error</h2>
                    <div className="sm (640px) py-2">
                        {errorMsg}
                    </div>
                    <button className="bg-red-500 hover:bg-blue-600 text-white py-2 px-4 mx-2 rounded-lg w-48" onClick={closeModal}>close</button>
                </Modal>
            </div>
            <div className="border p-6 rounded-lg bg-white shadow-md w-96 relative">
                <Link to="/" className="absolute top-2 right-2 text-gray-600 text-sm hover:text-blue-600">
                    Back
                </Link>
                <h1 className="text-2xl font-bold mb-4">Share a file with others!</h1>

                {/* TTL Input */}
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">
                        TTL (in days):
                    </label>
                    <input
                        type="number"
                        min="1"
                        value={ttl}
                        onChange={(e) => setTtl(e.target.value)}
                        className="mt-1 p-2 w-full border rounded-md focus:ring focus:ring-opacity-50"
                    />
                </div>

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
