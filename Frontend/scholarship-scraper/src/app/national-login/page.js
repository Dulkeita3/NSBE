"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { signInWithEmailAndPassword, signOut, onAuthStateChanged } from "firebase/auth";
import { auth } from "../firebase/firebaseConfig"; // Import Firebase auth
import { fetchUserData } from "../firebase/firebaseUserService"; // Fetch user data
import BackToHome from "../components/BackToHomeButton";

export default function National() {
    const [userData, setUserData] = useState(null);
    const [email, setEmail] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [error, setError] = useState(null);
    const router = useRouter();

    // ✅ Check if user is already logged in on page load
    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, async (user) => {
            if (user) {
                const userInfo = await fetchUserData(user.email);
                if (userInfo) {
                    setUserData(userInfo);
                    setIsLoggedIn(true);
                    localStorage.setItem("user", JSON.stringify(userInfo)); // Store session
                }
            } else {
                setIsLoggedIn(false);
                setUserData(null);
            }
        });

        return () => unsubscribe();
    }, []);

    // ✅ Handle Login with Firebase Auth
    const handleLogin = async (event) => {
        event.preventDefault();
        setError(null);

        try {
            const userCredential = await signInWithEmailAndPassword(auth, email + "@psu.edu", "defaultPassword123");
            const user = userCredential.user;

            // ✅ Fetch user data from Firestore
            const userInfo = await fetchUserData(user.email);
            if (userInfo) {
                setUserData(userInfo);
                setIsLoggedIn(true);
                localStorage.setItem("user", JSON.stringify(userInfo)); // Persist session
            } else {
                throw new Error("User data not found.");
            }
        } catch (error) {
            console.error("Login error:", error.message);
            setError("Invalid login. Please try again.");
        }
    };

    // ✅ Handle Logout
    const handleLogout = async () => {
        await signOut(auth);
        localStorage.removeItem("user");
        setUserData(null);
        setIsLoggedIn(false);
        setEmail("");
        router.push("/national-login");
    };

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
            <BackToHome />
            {isLoggedIn ? (
                <div className="max-w-lg mx-auto bg-white p-8 rounded-2xl shadow-lg text-center">
                    <h1 className="text-4xl font-extrabold mb-4 text-blue-700">🎉 Headed To Nationals!</h1>
                    <p className="text-gray-600 text-lg mb-6">
                        Hello, <span className="font-semibold text-gray-800">{userData?.firstname || "User"}</span>!
                        Get ready for an amazing experience.
                    </p>

                    <div className="w-full h-[2px] bg-gray-200 mb-6"></div>

                    {/* Navigation Buttons */}
                    <div className="flex flex-col gap-4">
                        <button
                            onClick={() => router.push("/national-room")}
                            className="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition duration-300 shadow-md"
                        >
                            🏨 View Roommates
                        </button>

                        <button
                            onClick={() => router.push("/national-itinerary")}
                            className="w-full bg-green-600 text-white font-semibold py-3 rounded-lg hover:bg-green-700 transition duration-300 shadow-md"
                        >
                            📅 View Itinerary
                        </button>

                        <button
                            onClick={() => router.push("/national-transit")}
                            className="w-full bg-yellow-600 text-white font-semibold py-3 rounded-lg hover:bg-yellow-700 transition duration-300 shadow-md"
                        >
                            🚍 View Transit
                        </button>

                        {/* Logout Button */}
                        <button
                            onClick={handleLogout}
                            className="w-full bg-red-600 text-white font-semibold py-3 rounded-lg hover:bg-red-700 transition duration-300 shadow-md"
                        >
                            🚪 Logout
                        </button>
                    </div>
                </div>
            ) : (
                <form onSubmit={handleLogin} className="max-w-sm mx-auto bg-white p-6 rounded-2xl shadow-lg">
                    <h2 className="text-xl font-semibold text-center mb-4 text-gray-800">Login</h2>

                    <div className="mb-4">
                        <label htmlFor="email" className="block text-gray-700 text-sm font-medium mb-1">
                            Enter your PSU Email ID
                        </label>
                        <input
                            type="input"
                            id="email"
                            name="email"
                            placeholder="abc123"
                            value={email.toLowerCase()}
                            onChange={(e) => setEmail(e.target.value.toLowerCase())}
                            className="text-gray-900 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                            required
                        />
                    </div>

                    {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

                    <button
                        type="submit"
                        className="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition duration-300"
                    >
                        Login
                    </button>
                </form>
            )}
        </div>
    );
}
