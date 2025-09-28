export interface CarthagoGPT {
  slug: string;
  name: string;
  description: string;
  tags: string[];
  featured?: boolean;
}

export const gpts: CarthagoGPT[] = [
  {
    slug: 'juriste',
    name: 'Juriste Virtuel',
    description: 'Conseils juridiques généraux pour les citoyens.',
    tags: ['droit', 'citoyen'],
    featured: true,
  },
  {
    slug: 'avocat',
    name: 'Avocat IA',
    description: 'Assistance avancée pour professionnels du droit.',
    tags: ['professionnel', 'procès'],
    featured: false,
  },
  {
    slug: 'lexico',
    name: 'LexicoGPT',
    description: 'Analyse et traduction de textes juridiques.',
    tags: ['traduction', 'analyse'],
    featured: true,
  },
];

export default gpts;
