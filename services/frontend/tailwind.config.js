import primeui from 'tailwindcss-primeui';

/** @type {import('tailwindcss').Config} */
export default {
    content: [],
    theme: {
        extend: {
            fontFamily: {
                sans: ['-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Fira Sans,Droid Sans,Helvetica Neue,sans-serif'],
            },
            
            keyframes: {
                slidein: {
                    from: {
                        opacity: "0",
                        transform: "translateX(60px)",
                    },
                    to: {
                        opacity: "1",
                        transform: "translateX(0px)",
                    },
                },

                slideout: {
                    from: {
                        opacity: "0",
                        transform: "translateX(-60px)",
                    },
                    to: {
                        opacity: "1",
                        transform: "translateX(0px)",
                    },
                },

                slidedown2: {
                    from: {
                        opacity: "0",
                        transform: "translateY(5px)",
                    },
                    to: {
                        opacity: "1",
                        transform: "translateY(0)",
                    },
                },

                animateHover: {
                    from: {
                        width: "100%",
                        left: "0%",
                    },
                    to: {
                        width: "120%",
                        left: "-10%"
                    },
                },
            },
            animation: {
                slidein: "slidein 1.1s ease var(--slidein-delay, 0) forwards",
                slideout: "slideout 1.2s ease var(--slideout-delay, 0) forwards",
                slidedown2: "slidedown2 1.1s ease var(--slidedown-delay, 0) forwards",
                animateHover: "animateHover 0.4s ease 9ms forwards",
            }
        },
    },
    darkMode: ['selector', '[class="p-dark"]'],
    plugins: [require('tailwindcss-primeui')],
}
