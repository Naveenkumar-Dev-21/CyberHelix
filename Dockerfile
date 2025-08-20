# AutoPenTest Docker Container
FROM kalilinux/kali-rolling:latest

LABEL maintainer="NaveeN"
LABEL description="AutoPenTest - Automated Penetration Testing Framework"
LABEL version="1.0"

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Python and build tools
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    # Security tools
    nmap \
    nikto \
    sqlmap \
    amass \
    theharvester \
    # Additional utilities
    curl \
    wget \
    git \
    dnsutils \
    net-tools \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Go (required for Nuclei)
RUN wget -O go.tar.gz https://go.dev/dl/go1.21.0.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go.tar.gz \
    && rm go.tar.gz

# Set Go environment
ENV PATH="/usr/local/go/bin:$PATH"
ENV GOPATH="/go"
ENV GOBIN="/go/bin"

# Install Nuclei
RUN go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
RUN nuclei -update-templates

# Install Metasploit (optional - large download)
# RUN curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall \
#     && chmod 755 msfinstall \
#     && ./msfinstall \
#     && rm msfinstall

# Create application directory
WORKDIR /app

# Create non-root user
RUN useradd -m -s /bin/bash autopentest && \
    chown -R autopentest:autopentest /app

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install development dependencies (optional)
ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then pip3 install --no-cache-dir -r requirements-dev.txt; fi

# Copy application code
COPY . .

# Set proper permissions
RUN chown -R autopentest:autopentest /app && \
    chmod +x autopentest.py

# Switch to non-root user
USER autopentest

# Create output directory
RUN mkdir -p /app/reports

# Set environment variables for tools
ENV NMAP_PATH=/usr/bin/nmap
ENV NUCLEI_PATH=/go/bin/nuclei
ENV NIKTO_PATH=/usr/bin/nikto
ENV SQLMAP_PATH=/usr/bin/sqlmap
ENV AMASS_PATH=/usr/bin/amass
ENV THEHARVESTER_PATH=/usr/bin/theHarvester
ENV OUTPUT_DIR=/app/reports

# Expose volume for reports
VOLUME ["/app/reports"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 autopentest.py --config-check || exit 1

# Default command
ENTRYPOINT ["python3", "autopentest.py"]
CMD ["--help"]

# Usage examples:
# Build: docker build -t autopentest .
# Run config check: docker run --rm autopentest --config-check
# Run scan: docker run --rm -v $(pwd)/reports:/app/reports autopentest scan example.com
# Interactive: docker run --rm -it --entrypoint /bin/bash autopentest
