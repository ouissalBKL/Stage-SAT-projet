import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatbotService } from '../services/chatbot.service';

interface Message {
  content: string;
  isUser: boolean;
  timestamp: Date;
}

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit, AfterViewInit {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;
  @ViewChild('questionInput') questionInput!: ElementRef;

  messages: Message[] = [];
  question: string = '';
  isLoading: boolean = false;
  showSpecialistModal: boolean = true;
  isSpecialist: boolean | null = null;

  constructor(private chatbotService: ChatbotService) {}

  ngOnInit() {
    // Message de bienvenue
    this.messages.push({
      content: "Bienvenue ! Je suis votre assistant virtuel en gestion des approvisionnements, prêt à vous accompagner.",
      isUser: false,
      timestamp: new Date()
    });
  }

  ngAfterViewInit() {
    this.scrollToBottom();
  }

  onSpecialistSelection(isSpecialist: boolean) {
    // Protection contre les clics multiples
    if (this.isSpecialist !== null) {
      return;
    }
    
    this.isSpecialist = isSpecialist;
    this.showSpecialistModal = false;
    
       // Ajouter un message de confirmation personnalisé (sans supprimer le message de bienvenue)
       const confirmationMessage = isSpecialist 
       ? "Vous êtes un spécialiste. Je vais adapter mes réponses à votre niveau d'expertise."
       : "Vous n'êtes pas spécialiste. Je vais vous expliquer les concepts de manière claire et accessible.";
     
    this.messages.push({
      content: confirmationMessage,
      isUser: false,
      timestamp: new Date()
    });
    
    this.scrollToBottom();
    
    // Appel au backend sans afficher sa réponse
    this.chatbotService.setSpecialist(isSpecialist).subscribe({
      next: (response) => {
        // Ne rien faire avec la réponse du backend
      },
      error: (error) => {
        console.error('Erreur lors de la définition du spécialiste:', error);
        alert('Erreur lors de l\'envoi de votre réponse.');
      }
    });
  }

  async askQuestion() {
    if (!this.question.trim()) return;
    
    if (this.isSpecialist === null) {
      alert("Veuillez d'abord répondre au mini questionnaire.");
      return;
    }

    // Supprimer le message de bienvenue s'il existe
    if (this.messages.length > 0 && this.messages[0].content.includes("Bienvenue")) {
      this.messages.shift();
    }

    // Ajouter le message de l'utilisateur
    this.messages.push({
      content: this.question,
      isUser: true,
      timestamp: new Date()
    });

    // Ajouter un message de chargement
    const loadingMessage: Message = {
      content: "Chargement...",
      isUser: false,
      timestamp: new Date()
    };
    this.messages.push(loadingMessage);
    this.scrollToBottom();

    this.isLoading = true;
    const userQuestion = this.question;
    this.question = '';

    try {
      const response = await this.chatbotService.askQuestion(userQuestion).toPromise();
      
      // Remplacer le message de chargement par la réponse
      this.messages[this.messages.length - 1] = {
        content: response.response || response.error || 'Erreur inconnue',
        isUser: false,
        timestamp: new Date()
      };
    } catch (error) {
      this.messages[this.messages.length - 1] = {
        content: "Erreur réseau.",
        isUser: false,
        timestamp: new Date()
      };
    } finally {
      this.isLoading = false;
      this.scrollToBottom();
    }
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.askQuestion();
    }
  }

  copyToClipboard(content: string) {
    navigator.clipboard.writeText(content).then(() => {
      // Optionnel: afficher un message de confirmation
    });
  }

  formatMessage(content: string): string {
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  }

  private scrollToBottom() {
    setTimeout(() => {
      if (this.messagesContainer) {
        this.messagesContainer.nativeElement.scrollTop = this.messagesContainer.nativeElement.scrollHeight;
      }
    }, 100);
  }
}
