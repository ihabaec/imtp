import { NextRequest, NextResponse } from "next/server";
import busboy from "busboy";
import { Readable } from "stream";

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const contentType = request.headers.get("content-type");
    if (!contentType || !contentType.includes("multipart/form-data")) {
      return NextResponse.json(
        { message: "Missing or invalid Content-Type header" },
        { status: 400 }
      );
    }

    const headers: Record<string, string> = {};
    request.headers.forEach((value, key) => {
      headers[key.toLowerCase()] = value;
    });

    return new Promise<NextResponse>((resolve, reject) => {
      const bb = busboy({
        headers,
        limits: { fileSize: 10 * 1024 * 1024 }, // 10MB limit
      });

      let hasFile = false;

      bb.on("file", (fieldname, file, info) => {
        const { filename, mimeType } = info;

        if (!["image/jpeg", "image/png"].includes(mimeType)) {
          return resolve(
            NextResponse.json(
              { message: "Invalid file type. Only JPEG and PNG are allowed." },
              { status: 400 }
            )
          );
        }

        hasFile = true;

        file.on("end", () => {
          console.log(`Processed file: ${filename}`);
        });
      });

      bb.on("finish", () => {
        if (!hasFile) {
          return resolve(
            NextResponse.json({ message: "No file uploaded" }, { status: 400 })
          );
        }

        resolve(
          NextResponse.json(
            { message: "File processed successfully" },
            { status: 200 }
          )
        );
      });

      bb.on("error", (err) => {
        console.error("Busboy error:", err);
        reject(
          NextResponse.json(
            { message: `Internal server error: ${err.message}` },
            { status: 500 }
          )
        );
      });

      const readable = Readable.fromWeb(request.body as any);
      readable.pipe(bb);
    });
  } catch (error: any) {
    console.error("Error processing file:", error);
    return NextResponse.json(
      { message: `Internal server error: ${error.message}` },
      { status: 500 }
    );
  }
}