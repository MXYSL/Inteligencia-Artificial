# Use your exact Node.js version to ensure perfect compatibility
FROM node:22.22.0-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package files first to leverage Docker's caching mechanism
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy all the remaining project files into the container
COPY . .

# Expose Vite's default development port
EXPOSE 5173

# Start the Vite dev server and expose it to the Docker network
CMD ["npm", "run", "dev", "--", "--host"]