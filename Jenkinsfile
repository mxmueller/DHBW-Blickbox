pipeline {
    agent any
    stages {
        stage('[GIT] 🔍 Checkout') {
            steps {
                checkout scm
            }
        }
        stage('[GIT] 🕵️ GitLeaks Scan') {
            steps {
                script {
                    def gitleaksExitCode = sh(script: '''
                        wget https://github.com/zricethezav/gitleaks/releases/download/v8.16.3/gitleaks_8.16.3_linux_x64.tar.gz
                        tar -xzf gitleaks_8.16.3_linux_x64.tar.gz
                        chmod +x gitleaks
                        ./gitleaks detect --source . -v --report-path gitleaks-report.json \
                        --exclude-files="**keys.json,**keys.txt" || true
                    ''', returnStatus: true)
                    if (gitleaksExitCode != 0) {
                        echo "GitLeaks may have found sensitive data. Please review the report."
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'gitleaks-report.json', fingerprint: true
                }
            }
        }
        stage('[ADA] 🛠️ Setup Build Environment') {
            steps {
                sh '''
                    sudo -n apt-get update
                    sudo -n apt-get install -y build-essential pkg-config libssl-dev libdbus-1-dev libudev-dev libdbus-glib-1-dev
                '''
            }
        }
        stage('[ADA] 🦀 Build') {
            steps {
                dir('blickbox/ada') {
                    sh '''
                        curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
                        export PATH="$HOME/.cargo/bin:$PATH"
                        rustc --version
                        cargo build --release
                    '''
                }
            }
        }
        
        stage('[ADA] 🧪 Test') {
            steps {
                dir('blickbox/ada') {
                    sh '''
                        export PATH="$HOME/.cargo/bin:$PATH"
                        cargo test
                    '''
                }
            }
        }
        stage('[ADA] 💅 Code formatting and linting') {
            steps {
                dir('blickbox/ada') {
                    script {
                        def clippyFlags = '''
                            -W clippy::all                     # Aktiviert alle Standard-Clippy-Lints
                            -W clippy::style                   # Aktiviert Stil-bezogene Lints
                            
                            -W clippy::clone_on_ref_ptr        # Warnt vor unnötigen .clone() Aufrufen
                            -W clippy::redundant_clone         # Warnt vor redundanten clone() Aufrufen
                            
                            -W clippy::suspicious              # Warnt vor verdächtigem Code
                            -W clippy::complexity              # Warnt vor übermäßig komplexem Code
                            
                            -A clippy::missing_docs_in_private_items # Erlaubt fehlende Dokumentation in privaten Items
                            -A clippy::module_name_repetitions # Erlaubt Modulnamenwiederholungen
                            -A clippy::too_many_arguments      # Erlaubt Funktionen mit vielen Argumenten
                            
                            -A clippy::never_type_fallback     # Ignoriert Warnungen bezüglich des Never-Type-Fallbacks
                            -A clippy::let_unit_value          # Ignoriert Warnungen für `let` Anweisungen mit Unit-Wert
                            -A clippy::uninlined_format_args   # Ignoriert Warnungen für nicht-inline Format-Argumente
                        '''.stripIndent()
                        
                        sh """
                            export PATH="$HOME/.cargo/bin:$PATH"
                            rustup component add clippy
                            cargo clippy -- ${clippyFlags}
                        """
                    }
                }
            }
            post {
                failure {
                    echo 'Clippy found issues. Please review the output above and fix the warnings/errors.'
                }
                success {
                    echo 'Clippy check passed successfully.'
                }
            }
        }
        stage('[ADA] 🛡️ Rust Security Audit') {
            steps {
                dir('blickbox/ada') {
                    sh '''
                        export PATH="$HOME/.cargo/bin:$PATH"
                        cargo install cargo-audit
                        cargo audit
                    '''
                }
            }
            post {
                success {
                    echo 'Rust security audit passed. No known vulnerabilities found.'
                }
                failure {
                    echo 'Rust security audit failed. Please review the vulnerabilities and update the dependencies.'
                }
            }
        }
        stage('[VALENTIN] 🛠️ Build') {
            steps {
                dir('server/client/valentin') {
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }
        
        stage('[VALENTIN] 💅 Code formatting and liniting') {
           steps {
                dir('server/client/valentin') {
                    sh 'npm install prettier --save-dev'
                    sh 'npx prettier --check "**/*.{js,jsx,ts,tsx,css,scss,md}"'
                }
            }
            post {
                failure {
                    echo 'run: npx prettier --write "**/*.{js,jsx,ts,tsx,css,scss,md}" to fix'
                }
            }
        }
        
        stage('[VALENTIN] 🧪 Jest Tests') {
            steps {
                dir('server/client/valentin') {
                    sh 'npm test'
                }
            }
            post {
                failure {
                    echo 'Jest tests failed. Please check the test results for more information.'
                }
            }
        }
        
        stage('[VALENTIN] 🛡️ Code Security Check') {
            steps {
                dir('server/client/valentin') {
                    sh 'npm install retire --save-dev'
                    sh 'npx retire --path . --outputformat json --outputpath ./retire-results.json'
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'server/client/valentin/retire-results.json', fingerprint: true
                }
                failure {
                    echo 'Retire.js hat veraltete Bibliotheken mit bekannten Schwachstellen gefunden. Bitte überprüfen Sie den Bericht.'
                }
            }
        }
        
        stage('[DOCKER] 🐳 Dockerfile Analysis') {
            steps {
                script {
                    sh '''
                        wget https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64
                        mv hadolint-Linux-x86_64 hadolint
                        chmod +x hadolint
                    '''

                    def dockerfiles = sh(script: 'find . -name Dockerfile', returnStdout: true).trim().split('\n')
                    
                    dockerfiles.each { dockerfile ->
                        echo "Analyzing Dockerfile: ${dockerfile}"
                        def hadolintExitCode = sh(script: "./hadolint ${dockerfile} || true", returnStatus: true)
                        if (hadolintExitCode != 0) {
                            echo "Hadolint found issues in ${dockerfile}. Please review the output above."
                        } else {
                            echo "${dockerfile} passed hadolint checks."
                        }
                    }
                }
            }
        }
    }
}
