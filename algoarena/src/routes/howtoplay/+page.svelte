<script>
    let currentStep = 0;
    
    const steps = [
      {
        titre: "1. Collectez vos ressources",
        gifUrl: "algoarena\\src\\routes\\howtoplay\\gifs\\tuto1.gif",
        description: "Vous commencerez la partie avec un Travailleur. Celui-ci vous permettera de collectionner les ressources (Arbre) sur la carte. Rammenez ces ressources dans votre chateau pour les ajouter à votre inventaire."
      },
      {
        titre: "2. Surveillez votre adversaire",
        gifUrl: "algoarena\\src\\routes\\howtoplay\\gifs\\tuto1.gif",
        description: "Avec vos ressources, construisez un Éclaireur qui vous permettera de voir ce que votre adversaire est en train de plannifier. Attention de ne pas le perdre au combat!"
      },
      {
        titre: "3. Rassemblez votre armée",
        gifUrl: "algoarena\\src\\routes\\howtoplay\\gifs\\tuto1.gif",
        description: "Maintenant que vous avez amasser des ressources et vous connaissez le plan de votre adversaire, c'est le temps d'attaquer. Construisez les unités de combat nécessaires pour contrez la stratégie opposante et obtenir la victoire."
      },
      {
        titre: "3.1 Unité Mélée",
        gifUrl: "algoarena\\src\\routes\\howtoplay\\gifs\\tuto1.gif",
        description: "Polyvalente et peu couteuse, cette unité peut être très utile au début du jeu."
      },
      {
        titre: "3.2 Unité Archer",
        gifUrl: "algoarena\\src\\routes\\howtoplay\\gifs\\tuto1.gif",
        description: "Cette unité attaque à distance et fonctionne le mieux lorsque protégée par d'autres unités ou dans des goulots d'étouffement."
      },
      {
        titre: "3.3 Unité Tank",
        gifUrl: "algoarena\\src\\routes\\howtoplay\\gifs\\tuto1.gif",
        description: "Comme son nom l'indique, cette unité peux absorber beaucoup de dégat avant de se faire détruire. En retour, elle ne fait pas beaucoup de dégat et est très couteuse."
      },
      {
        titre: "3.4 Unité Cannon",
        gifUrl: "algoarena\\src\\routes\\howtoplay\\gifs\\tuto1.gif",
        description: "Cette unité est la plus couteuse en ressources et la plus facile à détruire. En échange, elle fait beaucoup plus de dégat à distance aux unités et aux structures adverses. Peut garantir une victoire, si utilisée correctement."
      },
      {
        titre: "4. Conditions de victoire",
        gifUrl: "algoarena\\src\\routes\\howtoplay\\gifs\\tuto1.gif",
        description: "Pour gagner la partie, il faut avoir détruit le chateau adverse, ou avoir détruit toutes les unitées adverses. Attention, car votre adversaire essayera de faire la même chose!"
      },
      
    ];
  
    function goToNextStep() {
      if (currentStep < steps.length - 1) {
        currentStep += 1;
      }
    }
  
    function goToPreviousStep() {
      if (currentStep > 0) {
        currentStep -= 1;
      }
    }
  </script>
  
  <div class="tutorial">
    <h2>{steps[currentStep].titre}</h2>
    <img src={steps[currentStep].gifUrl} alt="Step GIF" />
    <p>{steps[currentStep].description}</p>
    
    <button on:click={goToPreviousStep} disabled={currentStep === 0}>Previous Step</button>
    <button on:click={goToNextStep} disabled={currentStep === steps.length - 1}>Next Step</button>
  </div>
  
  <style>
    /* TODO rajouter style */
  </style>