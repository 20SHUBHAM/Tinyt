// Focus Group specific functionality

class FocusGroupWorkflow {
    constructor(app) {
        this.app = app;
        this.bindWorkflowEvents();
    }
    
    bindWorkflowEvents() {
        // Step 1: Persona Generation
        document.getElementById('generatePersonas')?.addEventListener('click', () => this.generatePersonas());
        document.getElementById('proceedToFramework')?.addEventListener('click', () => this.app.goToStep(2));
        
        // Step 2: Framework Generation
        document.getElementById('generateFramework')?.addEventListener('click', () => this.generateFramework());
        document.getElementById('proceedToSimulation')?.addEventListener('click', () => this.app.goToStep(3));
        
        // Step 3: Simulation
        document.getElementById('runSimulation')?.addEventListener('click', () => this.runSimulation());
        document.getElementById('proceedToSummary')?.addEventListener('click', () => this.app.goToStep(4));
        
        // Step 4: Summary Generation
        document.getElementById('generateSummary')?.addEventListener('click', () => this.generateSummary());
        document.getElementById('generateAnotherSummary')?.addEventListener('click', () => this.generateSummary());
        document.getElementById('downloadSummary')?.addEventListener('click', () => this.downloadSummary());
        document.getElementById('proceedToQA')?.addEventListener('click', () => this.app.goToStep(5));
        
        // Step 5: Q&A
        document.getElementById('askQuestion')?.addEventListener('click', () => this.askQuestion());
        document.getElementById('userQuestion')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.askQuestion();
            }
        });
        document.getElementById('exportSession')?.addEventListener('click', () => this.exportSession());
        
        // Dynamic event delegation for edit buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('.edit-persona-btn, .edit-persona-btn *')) {
                const btn = e.target.closest('.edit-persona-btn');
                const personaId = btn.dataset.personaId;
                this.editPersona(personaId);
            }
            
            if (e.target.matches('.suggested-question')) {
                const question = e.target.textContent;
                document.getElementById('userQuestion').value = question;
                this.askQuestion();
            }
        });
    }
    
    async generatePersonas() {
        const description = document.getElementById('audienceDescription').value.trim();
        const numPersonas = parseInt(document.getElementById('numPersonas').value);
        
        if (!description) {
            this.app.showAlert('Please provide a description of your target audience.', 'warning');
            return;
        }
        
        const loading = this.app.showLoading(
            'Generating Personas...', 
            'Creating diverse, realistic personas based on your description.'
        );
        
        try {
            const result = await this.app.apiCall('/api/generate-personas', 'POST', {
                description: description,
                num_personas: numPersonas
            });
            
            this.app.sessionData.sessionId = result.session_id;
            this.app.sessionData.personas = result.personas;
            
            this.displayPersonas(result.personas);
            this.app.showAlert('Personas generated successfully!', 'success');
            
        } catch (error) {
            console.error('Error generating personas:', error);
            this.app.showAlert('Failed to generate personas: ' + error.message, 'danger');
        } finally {
            this.app.hideLoading();
        }
    }
    
    displayPersonas(personas) {
        const container = document.getElementById('personasList');
        const display = document.getElementById('personasDisplay');
        
        container.innerHTML = personas.map(persona => this.app.formatPersonaCard(persona)).join('');
        display.style.display = 'block';
        
        // Scroll to show the personas
        display.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    async editPersona(personaId) {
        const persona = this.app.sessionData.personas.find(p => p.id === personaId);
        if (!persona) return;
        
        // Simple edit modal (could be enhanced with a proper modal)
        const newName = prompt('Edit persona name:', persona.name);
        if (newName && newName !== persona.name) {
            const loading = this.app.showLoading('Updating persona...');
            
            try {
                persona.name = newName;
                await this.app.apiCall('/api/update-persona', 'POST', {
                    persona_id: personaId,
                    persona: persona
                });
                
                this.displayPersonas(this.app.sessionData.personas);
                this.app.showAlert('Persona updated successfully!', 'success');
                
            } catch (error) {
                this.app.showAlert('Failed to update persona: ' + error.message, 'danger');
            } finally {
                this.app.hideLoading();
            }
        }
    }
    
    async generateFramework() {
        const topic = document.getElementById('discussionTopic').value.trim();
        const businessContext = document.getElementById('businessContext').value.trim();
        const duration = parseInt(document.getElementById('sessionDuration').value);
        
        if (!topic) {
            this.app.showAlert('Please provide a discussion topic.', 'warning');
            return;
        }
        
        if (!businessContext) {
            this.app.showAlert('Please provide business context and goals.', 'warning');
            return;
        }
        
        const loading = this.app.showLoading(
            'Generating Framework...', 
            'Creating structured discussion phases with business-focused questions.'
        );
        
        try {
            const result = await this.app.apiCall('/api/generate-framework', 'POST', {
                topic: topic,
                business_context: businessContext,
                duration: duration
            });
            
            this.app.sessionData.framework = result.framework;
            this.displayFramework(result.framework);
            this.app.showAlert('Discussion framework generated successfully!', 'success');
            
        } catch (error) {
            console.error('Error generating framework:', error);
            this.app.showAlert('Failed to generate framework: ' + error.message, 'danger');
        } finally {
            this.app.hideLoading();
        }
    }
    
    displayFramework(framework) {
        const container = document.getElementById('frameworkContent');
        const display = document.getElementById('frameworkDisplay');
        
        const phases = framework.discussion_phases || [];
        
        let html = `
            <div class="mb-3">
                <h6>Session Overview</h6>
                <div class="summary-content">
                    <p><strong>Duration:</strong> ${framework.duration_minutes} minutes</p>
                    <p><strong>Objectives:</strong></p>
                    <ul>
                        ${(framework.session_overview?.objectives || []).map(obj => `<li>${obj}</li>`).join('')}
                    </ul>
                </div>
            </div>
            
            <h6>Discussion Phases</h6>
            ${phases.map((phase, index) => this.app.formatFrameworkPhase(phase, index)).join('')}
        `;
        
        container.innerHTML = html;
        display.style.display = 'block';
        
        // Scroll to show the framework
        display.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    async runSimulation() {
        if (!this.app.sessionData.personas.length || !this.app.sessionData.framework) {
            this.app.showAlert('Please complete persona generation and framework creation first.', 'warning');
            return;
        }
        
        const loading = this.app.showLoading(
            'Running Simulation...', 
            'TinyTroupe agents are conducting a realistic focus group discussion. This may take several minutes.'
        );
        
        try {
            // Update UI to show simulation in progress
            document.getElementById('simulationStatus').innerHTML = `
                <div class="text-center py-5">
                    <div class="spinner-border text-warning mb-3" role="status">
                        <span class="visually-hidden">Running simulation...</span>
                    </div>
                    <p class="lead">Simulation in progress...</p>
                    <p class="text-muted">AI agents are having a realistic discussion based on your personas and framework.</p>
                </div>
            `;
            
            const result = await this.app.apiCall('/api/run-simulation', 'POST', {});
            
            this.app.sessionData.simulation = result.simulation;
            this.displaySimulationResults(result.simulation);
            this.app.showAlert('Focus group simulation completed successfully!', 'success');
            
        } catch (error) {
            console.error('Error running simulation:', error);
            this.app.showAlert('Failed to run simulation: ' + error.message, 'danger');
            
            // Reset simulation status
            document.getElementById('simulationStatus').innerHTML = `
                <p class="lead">Simulation failed. Please try again.</p>
                <button class="btn btn-warning btn-lg" id="runSimulation">
                    <i class="bi bi-play-circle me-2"></i>
                    Retry Simulation
                </button>
            `;
            
        } finally {
            this.app.hideLoading();
        }
    }
    
    displaySimulationResults(simulation) {
        const conversationLog = simulation.simulation_results?.conversation_log || [];
        const analysis = simulation.analysis || {};
        
        // Display conversation
        const logContainer = document.getElementById('conversationLog');
        logContainer.innerHTML = conversationLog
            .map(item => this.app.formatConversationItem(item))
            .join('');
        
        // Display live analysis
        const analysisContainer = document.getElementById('liveAnalysis');
        analysisContainer.innerHTML = `
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">${simulation.participants || 0}</div>
                    <div class="metric-label">Participants</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${simulation.metadata?.total_interactions || 0}</div>
                    <div class="metric-label">Interactions</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${simulation.metadata?.spontaneous_moments || 0}</div>
                    <div class="metric-label">Spontaneous</div>
                </div>
            </div>
            
            <h6>Key Themes</h6>
            ${(analysis.key_themes || []).map(theme => `
                <div class="insight-item">${theme}</div>
            `).join('')}
            
            <h6>Discussion Quality</h6>
            <div class="summary-content">
                <p><strong>Engagement:</strong> ${analysis.discussion_quality?.engagement_level || 'Unknown'}</p>
                <p><strong>Summary:</strong> ${analysis.discussion_quality?.group_dynamics_summary || 'No summary available'}</p>
            </div>
        `;
        
        // Show results
        document.getElementById('simulationStatus').style.display = 'none';
        document.getElementById('simulationResults').style.display = 'block';
        
        // Auto-scroll conversation to bottom
        logContainer.scrollTop = logContainer.scrollHeight;
    }
    
    async generateSummary() {
        if (!this.app.sessionData.simulation) {
            this.app.showAlert('Please run the simulation first.', 'warning');
            return;
        }
        
        const summaryType = document.getElementById('summaryType').value;
        const customSections = document.getElementById('customSections').value.trim();
        
        const loading = this.app.showLoading(
            'Generating Summary...', 
            'Creating a customized report based on the focus group discussion.'
        );
        
        try {
            const summarySchema = {
                type: summaryType,
                custom_sections: summaryType === 'custom' ? customSections : undefined
            };
            
            const result = await this.app.apiCall('/api/generate-summary', 'POST', {
                summary_schema: summarySchema
            });
            
            this.app.sessionData.summaries.push(result.summary);
            this.displaySummary(result.summary);
            this.app.showAlert('Summary generated successfully!', 'success');
            
        } catch (error) {
            console.error('Error generating summary:', error);
            this.app.showAlert('Failed to generate summary: ' + error.message, 'danger');
        } finally {
            this.app.hideLoading();
        }
    }
    
    displaySummary(summary) {
        const container = document.getElementById('summaryContent');
        const display = document.getElementById('summaryDisplay');
        
        container.innerHTML = this.app.formatSummaryContent(summary);
        display.style.display = 'block';
        
        // Scroll to show the summary
        display.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    downloadSummary() {
        if (this.app.sessionData.summaries.length === 0) {
            this.app.showAlert('No summary available to download.', 'warning');
            return;
        }
        
        const latestSummary = this.app.sessionData.summaries[this.app.sessionData.summaries.length - 1];
        const filename = `focus-group-summary-${new Date().toISOString().slice(0, 10)}.json`;
        
        this.app.downloadJSON(latestSummary, filename);
        this.app.showAlert('Summary downloaded successfully!', 'success');
    }
    
    async askQuestion() {
        const question = document.getElementById('userQuestion').value.trim();
        
        if (!question) {
            this.app.showAlert('Please enter a question.', 'warning');
            return;
        }
        
        if (!this.app.sessionData.simulation) {
            this.app.showAlert('Please run the simulation first.', 'warning');
            return;
        }
        
        const loading = this.app.showLoading(
            'Processing Question...', 
            'Analyzing the discussion to provide an evidence-based answer.'
        );
        
        try {
            const result = await this.app.apiCall('/api/ask-question', 'POST', {
                question: question
            });
            
            this.app.sessionData.qaHistory.push({
                question: question,
                answer: result.answer,
                timestamp: new Date().toISOString()
            });
            
            this.displayQAItem(question, result.answer);
            
            // Clear the question input
            document.getElementById('userQuestion').value = '';
            
            this.app.showAlert('Question answered successfully!', 'success');
            
        } catch (error) {
            console.error('Error asking question:', error);
            this.app.showAlert('Failed to process question: ' + error.message, 'danger');
        } finally {
            this.app.hideLoading();
        }
    }
    
    displayQAItem(question, answer) {
        const container = document.getElementById('qaHistory');
        
        const qaHtml = `
            <div class="qa-item">
                <div class="question-text">Q: ${question}</div>
                <div class="answer-text">A: ${answer.direct_answer}</div>
                
                ${answer.supporting_evidence && answer.supporting_evidence.length > 0 ? `
                    <div class="supporting-evidence">
                        <small><strong>Supporting Evidence:</strong></small>
                        ${answer.supporting_evidence.map(evidence => `
                            <div class="evidence-item">
                                <small><strong>${evidence.source}:</strong> ${evidence.content}</small>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
                
                ${answer.implications && answer.implications.length > 0 ? `
                    <div class="mt-2">
                        <small><strong>Implications:</strong></small>
                        <ul class="small">
                            ${answer.implications.map(imp => `<li>${imp}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                <div class="mt-2">
                    <small class="text-muted">
                        Confidence: ${answer.confidence_level} • 
                        ${new Date().toLocaleTimeString()}
                    </small>
                </div>
            </div>
        `;
        
        container.insertAdjacentHTML('beforeend', qaHtml);
        
        // Scroll to show the new Q&A
        container.lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    async loadSuggestedQuestions() {
        if (!this.app.sessionData.simulation) return;
        
        try {
            const result = await this.app.apiCall('/api/suggest-questions', 'GET');
            
            const container = document.getElementById('suggestedQuestions');
            container.innerHTML = result.suggestions
                .slice(0, 6) // Show first 6 suggestions
                .map(suggestion => `
                    <span class="suggested-question" title="${suggestion.rationale}">
                        ${suggestion.question}
                    </span>
                `).join('');
                
        } catch (error) {
            console.error('Error loading suggested questions:', error);
        }
    }
    
    async exportSession() {
        if (!this.app.sessionData.sessionId) {
            this.app.showAlert('No session data to export.', 'warning');
            return;
        }
        
        const loading = this.app.showLoading('Exporting Session...', 'Preparing complete session data for download.');
        
        try {
            const result = await this.app.apiCall('/api/export-session', 'GET');
            
            const filename = this.app.generateSessionFilename();
            this.app.downloadJSON(result.data, filename);
            
            this.app.showAlert('Session exported successfully!', 'success');
            
        } catch (error) {
            console.error('Error exporting session:', error);
            this.app.showAlert('Failed to export session: ' + error.message, 'danger');
        } finally {
            this.app.hideLoading();
        }
    }
}

// Initialize workflow when the main app is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait for the main app to be initialized
    setTimeout(() => {
        if (window.focusGroupApp) {
            window.focusGroupWorkflow = new FocusGroupWorkflow(window.focusGroupApp);
            
            // Load suggested questions when reaching step 5
            const originalGoToStep = window.focusGroupApp.goToStep;
            window.focusGroupApp.goToStep = function(stepNumber) {
                originalGoToStep.call(this, stepNumber);
                
                if (stepNumber === 5 && window.focusGroupWorkflow) {
                    window.focusGroupWorkflow.loadSuggestedQuestions();
                }
            };
        }
    }, 100);
});