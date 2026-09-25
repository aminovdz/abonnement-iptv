import { defineCollection, z } from 'astro:content';

const guidesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string().default('Équipe Technique France IPTV'),
    image: z.string().default('/images/hero-bg.webp'),
    imageAlt: z.string().default('Abonnement IPTV France — Guide et Tutoriel'),
    tags: z.array(z.string()).default(['Abonnement IPTV', 'IPTV France', 'Streaming 4K', 'Tutoriel']),
    featured: z.boolean().default(false),
    readingTime: z.string().default('6 min de lecture'),
    category: z.string().default('Guides & Tutoriels'),
    targetKeyword: z.string().optional()
  })
});

export const collections = {
  guides: guidesCollection
};
