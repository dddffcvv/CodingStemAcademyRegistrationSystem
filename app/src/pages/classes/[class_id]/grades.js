import {Layout} from "@/app/layout";
import React, { useEffect, useState } from 'react';
import {Card} from "@/components/ui/card";
import {useRouter} from "next/router";

export default function Grades() {
  const router = useRouter();
  const { class_id } = router.query;

  return (
    <Layout title={"Grades"}>
      <div className="flex flex-1 flex-col gap-4 p-4">
        <div className="grid auto-rows-min gap-4 md:grid-cols-3">
          <Card className={"p-4"}>
            <p>This is the grades page for grades {class_id}.</p>
          </Card>
        </div>
        <div className="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min" />
      </div>
    </Layout>
  );
}
