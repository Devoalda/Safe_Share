import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router for navigation

function HomePage() {
    return (
        <div className="h-screen flex flex-col items-center justify-center bg-gray-100">
            <div className="text-3xl text-gray-800 text-center my-10">SafeShare</div>

            <div className="text-center">
                <div className="mb-4">
                    <Link to="/upload" className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 mx-2 rounded-lg w-48">
                        Upload a File
                    </Link>
                </div>
                <div>
                    <Link to="/download" className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 mx-2 rounded-lg w-48">
                        Download a File
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default HomePage;
