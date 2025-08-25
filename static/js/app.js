// Main application JavaScript for Agentic Focus Group Platform

class FocusGroupApp {
    constructor() {
        this.currentStep = 1;
        this.sessionData = {
            sessionId: null,
            personas: [],
            framework: null,
            simulation: null,
            summaries: [],
            qaHistory: []
        };
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.initializeInterface();
    }
    
    bindEvents() {
        // Navigation events
        document.getElementById('startNewSession')?.addEventListener('click', () => this.startNewSession());
        document.getElementById('newSessionBtn')?.addEventListener('click', () => this.startNewSession());
        
        // Step navigation
        document.addEventListener('click', (e) => {
            if (e.target.matches('.step[data-step]')) {
                const step = parseInt(e.target.dataset.step);
                if (step <= this.currentStep) {
                    this.goToStep(step);
                }
            }
        });
        
        // Handle summary type change
        document.getElementById('summaryType')?.addEventListener('change', (e) => {
            const customOptions = document.getElementById('customSummaryOptions');
            if (e.target.value === 'custom') {
                customOptions.style.display = 'block';
            } else {
                customOptions.style.display = 'none';
            }
        });
    }
    
    initializeInterface() {
        // Hide main app initially
        const mainApp = document.getElementById('mainApp');
        if (mainApp) {
            mainApp.style.display = 'none';
        }
    }
    
    startNewSession() {
        // Show main app
        document.getElementById('mainApp').style.display = 'block';
        document.getElementById('featuresSection').style.display = 'none';
        
        // Reset session data
        this.sessionData = {
            sessionId: null,
            personas: [],
            framework: null,
            simulation: null,
            summaries: [],
            qaHistory: []
        };
        
        // Start from step 1
        this.goToStep(1);
        
        // Scroll to top
        window.scrollTo(0, 0);
    }
    
    goToStep(stepNumber) {
        // Update current step
        this.currentStep = stepNumber;
        
        // Update step indicator
        document.querySelectorAll('.step').forEach((step, index) => {
            const stepNum = index + 1;
            step.classList.remove('active', 'completed');
            
            if (stepNum === stepNumber) {
                step.classList.add('active');
            } else if (stepNum < stepNumber) {
                step.classList.add('completed');
            }
        });
        
        // Show correct step content
        document.querySelectorAll('.step-content').forEach((content, index) => {
            const stepNum = index + 1;
            content.classList.remove('active');
            
            if (stepNum === stepNumber) {
                content.classList.add('active');
            }
        });
        
        // Scroll to top of step
        document.querySelector('.step-content.active').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }
    
    showLoading(text = 'Processing...', subtext = 'Please wait while we process your request.') {
        const modal = document.getElementById('loadingModal');
        document.getElementById('loadingText').textContent = text;
        document.getElementById('loadingSubtext').textContent = subtext;
        
        const modalInstance = new bootstrap.Modal(modal);
        modalInstance.show();
        
        return modalInstance;
    }
    
    hideLoading() {
        const modal = document.getElementById('loadingModal');
        const modalInstance = bootstrap.Modal.getInstance(modal);
        if (modalInstance) {
            modalInstance.hide();
        }
    }
    
    showAlert(message, type = 'info', duration = 5000) {
        const alertContainer = document.getElementById('alertContainer');
        const alertId = 'alert-' + Date.now();
        
        const alertHtml = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        alertContainer.insertAdjacentHTML('beforeend', alertHtml);
        
        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                const alert = document.getElementById(alertId);
                if (alert) {
                    const alertInstance = bootstrap.Alert.getInstance(alert);
                    if (alertInstance) {
                        alertInstance.close();
                    }
                }
            }, duration);
        }
    }
    
    async apiCall(endpoint, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(endpoint, options);
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error || 'API request failed');
            }
            
            return result;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
    
    formatPersonaCard(persona) {
        const demographics = persona.demographics || {};
        const traits = persona.psychographics?.personality_traits || [];
        const style = persona.discussion_style || {};
        
        return `
            <div class="col-md-6 col-lg-4">
                <div class="persona-card" data-persona-id="${persona.id}">
                    <h6>${persona.name}</h6>
                    
                    <div class="persona-demographics">
                        <small><strong>Age:</strong> ${demographics.age || 'N/A'}</small><br>
                        <small><strong>Occupation:</strong> ${demographics.occupation || 'N/A'}</small><br>
                        <small><strong>Location:</strong> ${demographics.location || 'N/A'}</small>
                    </div>
                    
                    <div class="mb-2">
                        <small><strong>Traits:</strong></small><br>
                        ${traits.map(trait => `<span class="persona-trait">${trait}</span>`).join('')}
                    </div>
                    
                    <div class="mb-2">
                        <small><strong>Participation:</strong> ${style.participation_level || 'Medium'}</small><br>
                        <small><strong>Style:</strong> ${style.speaking_style || 'Conversational'}</small>
                    </div>
                    
                    ${persona.background_story ? `
                        <div class="mt-2">
                            <small class="text-muted">${persona.background_story.substring(0, 150)}...</small>
                        </div>
                    ` : ''}
                    
                    <div class="mt-3">
                        <button class="btn btn-outline-primary btn-sm edit-persona-btn" data-persona-id="${persona.id}">
                            <i class="bi bi-pencil me-1"></i>Edit
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    formatFrameworkPhase(phase, index) {
        const questions = phase.primary_questions || [];
        const probes = phase.follow_up_probes || [];
        
        return `
            <div class="framework-phase">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <h6>Phase ${index + 1}: ${phase.name}</h6>
                    <span class="badge bg-secondary">${phase.duration_minutes || 0} min</span>
                </div>
                
                <p class="text-muted mb-3">${phase.objective}</p>
                
                <div class="phase-questions">
                    <small><strong>Primary Questions:</strong></small>
                    ${questions.map(q => `
                        <div class="question-item">
                            <div class="fw-semibold">${q.question}</div>
                            ${q.rationale ? `<small class="text-muted">${q.rationale}</small>` : ''}
                        </div>
                    `).join('')}
                    
                    ${probes.length > 0 ? `
                        <small class="mt-2"><strong>Follow-up Probes:</strong></small>
                        ${probes.map(p => `
                            <div class="question-item">
                                <div>${p.probe}</div>
                                <small class="text-muted">When: ${p.trigger}</small>
                            </div>
                        `).join('')}
                    ` : ''}
                </div>
            </div>
        `;
    }
    
    formatConversationItem(item) {
        const typeClass = item.type?.includes('moderator') ? 'moderator' : 
                         item.type?.includes('spontaneous') ? 'spontaneous' : 'participant';
        
        const timestamp = new Date(item.timestamp).toLocaleTimeString();
        
        return `
            <div class="conversation-item ${typeClass}">
                <div class="speaker-name">${item.speaker}</div>
                <div class="conversation-content">${item.content}</div>
                <div class="conversation-meta">
                    ${timestamp} • ${item.type || 'comment'}
                    ${item.phase ? ` • ${item.phase}` : ''}
                </div>
            </div>
        `;
    }
    
    formatSummaryContent(summary) {
        if (summary.summary_type === 'executive') {
            return this.formatExecutiveSummary(summary);
        } else if (summary.summary_type === 'detailed') {
            return this.formatDetailedReport(summary);
        } else if (summary.summary_type === 'insights_only') {
            return this.formatInsightsSummary(summary);
        } else {
            return this.formatComprehensiveSummary(summary);
        }
    }
    
    formatExecutiveSummary(summary) {
        return `
            <div class="summary-section">
                <h5>Executive Overview</h5>
                <div class="summary-content">
                    ${summary.executive_overview || 'Overview not available'}
                </div>
            </div>
            
            <div class="summary-section">
                <h5>Key Findings</h5>
                <div class="summary-content">
                    <ul>
                        ${(summary.key_findings || []).map(finding => `<li>${finding}</li>`).join('')}
                    </ul>
                </div>
            </div>
            
            <div class="summary-section">
                <h5>Recommended Actions</h5>
                <div class="summary-content">
                    ${(summary.recommended_actions || []).map(action => `
                        <div class="recommendation-item priority-${action.priority || 'medium'}">
                            <div class="fw-semibold">${action.action}</div>
                            <small class="text-muted">
                                Priority: ${action.priority} • Timeline: ${action.timeline}
                            </small>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    formatDetailedReport(summary) {
        // Format detailed report structure
        return `
            <div class="summary-content">
                <h5>Detailed Research Report</h5>
                <pre style="white-space: pre-wrap; font-family: inherit;">${JSON.stringify(summary, null, 2)}</pre>
            </div>
        `;
    }
    
    formatInsightsSummary(summary) {
        return `
            <div class="summary-section">
                <h5>Core Consumer Insights</h5>
                <div class="summary-content">
                    ${(summary.core_consumer_insights || []).map(insight => `
                        <div class="insight-item">${insight}</div>
                    `).join('')}
                </div>
            </div>
            
            <div class="summary-section">
                <h5>Actionable Intelligence</h5>
                <div class="summary-content">
                    ${(summary.actionable_takeaways || []).map(takeaway => `
                        <div class="insight-item">${takeaway}</div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    formatComprehensiveSummary(summary) {
        return `
            <div class="summary-content">
                <h5>Comprehensive Summary</h5>
                <pre style="white-space: pre-wrap; font-family: inherit;">${JSON.stringify(summary, null, 2)}</pre>
            </div>
        `;
    }
    
    downloadJSON(data, filename) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    generateSessionFilename() {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        return `focus-group-session-${timestamp}.json`;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.focusGroupApp = new FocusGroupApp();
});