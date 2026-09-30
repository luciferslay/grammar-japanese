import LevelHome from '@/components/level-home';
import { DEFAULT_LEVEL } from '@/lib/lessons';

export default function Home({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  return <LevelHome slug={DEFAULT_LEVEL} searchParams={searchParams} />;
}
