import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

// Sélectionner le bouton qui déclenche la génération de PDF
const generatePdfButton = document.getElementById('imprimer');

// Ajouter un événement de clic sur le bouton
generatePdfButton.addEventListener('click', () => {
  // Sélectionner la div qui contient la facture
  const element = document.getElementById('main-content');

  // Créer une capture d'écran de la div avec html2canvas
  html2canvas(element).then(canvas => {
    // Créer une instance de jsPDF
    const pdf = new jsPDF();

    // Ajouter l'image au PDF
    pdf.addImage(canvas.toDataURL('image/jpeg'), 'JPEG', 0, 0);

    // Enregistrer le fichier PDF
    pdf.save('facture.pdf');
  });
});